"""
Local Jev-Compatible Intent Classifier for Merchant Intelligence Router.

NOTE: This is a local compatible implementation running via scikit-learn (TF-IDF + Cosine Similarity)
at zero cost. It is designed for learning and local development, and is NOT the official TypeSafe AI Jev service.
It implements the BaseIntentClassifier interface so it can be seamlessly swapped with RealJevClassifier later.
"""

import re
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.choices import Choice, MERCHANT_CHOICES
from app.state import Intent, ClassificationResult, MerchantState

# Synonym expansions to enhance lexical coverage without external APIs
SYNONYM_MAP: Dict[str, str] = {
    # Analytics synonyms
    "turnover": "sales revenue",
    "earnings": "sales revenue",
    "profit": "sales revenue",
    "income": "sales revenue",
    "fluctuation": "trend sales drop",
    "fell": "drop low sales",
    "fallen": "drop low sales",
    "dropped": "drop low sales",
    # Inventory synonyms
    "remaining": "left stock available quantity",
    "restock": "reorder low stock inventory",
    "replenish": "reorder low stock inventory",
    "shortage": "low stock out of stock inventory",
    # Customer synonyms
    "buyer": "customer",
    "buyers": "customers",
    "client": "customer",
    "clients": "customers",
    "purchaser": "customer",
    "shopper": "customer",
    # Products synonyms
    "sku": "product item",
    "skus": "products items",
    "bestseller": "best selling product top",
    "bestsellers": "best selling products top",
}

# Domain intent signals to distinguish meaningful queries from purely vague/generic chat
AMBIGUOUS_PATTERNS = [
    r"^show me something useful$",
    r"^tell me about my business$",
    r"^what should i know\??$",
    r"^give me an update$",
    r"^tell me the history.*$"
]


def normalize_text(text: str) -> str:
    """
    Normalizes input text: lowercases, strips whitespace, standardizes punctuation,
    and expands domain-specific merchant synonyms.
    """
    if not text:
        return ""
    cleaned = text.lower().strip()
    cleaned = re.sub(r'[^a-z0-9\s]', ' ', cleaned)
    tokens = [w for w in cleaned.split() if w]
    
    expanded_tokens = []
    for token in tokens:
        if token in SYNONYM_MAP:
            expanded_tokens.append(SYNONYM_MAP[token])
        else:
            expanded_tokens.append(token)
            
    return " ".join(expanded_tokens)


class BaseIntentClassifier(ABC):
    """
    Abstract Base Class for Intent Classifiers.
    Defines the standard interface allowing zero-downtime substitution between
    local heuristic/TF-IDF classifiers and remote TypeSafe/Jev APIs.
    """

    @abstractmethod
    def classify(self, message: str) -> ClassificationResult:
        """Classify user query and return a typed ClassificationResult."""
        pass

    @abstractmethod
    def explain(self, message: str) -> Dict[str, Any]:
        """Provide detailed score breakdown for debugging and inspection."""
        pass


class JevCompatibleClassifier(BaseIntentClassifier):
    """
    Zero-cost local classifier utilizing TF-IDF and Cosine Similarity over typed Choices.
    Simulates Jev's fast categorical probability estimation without calling external paid APIs.
    """

    def __init__(self, choices: Optional[List[Choice]] = None, confidence_threshold: float = 0.70):
        self.choices = choices or MERCHANT_CHOICES
        self.confidence_threshold = confidence_threshold
        self._corpus: List[str] = []
        self._corpus_labels: List[str] = []
        self._fit_vectorizer()

    def _fit_vectorizer(self) -> None:
        """Builds TF-IDF index across all choice examples and descriptions."""
        self._corpus = []
        self._corpus_labels = []

        for choice in self.choices:
            # Include description for semantic background
            self._corpus.append(normalize_text(choice.description))
            self._corpus_labels.append(choice.name)

            # Include each representative example phrase
            for example in choice.examples:
                self._corpus.append(normalize_text(example))
                self._corpus_labels.append(choice.name)

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self._corpus)

    def _calculate_scores(self, message: str) -> Dict[str, float]:
        """Calculates aggregated cosine similarity scores for each intent."""
        norm_msg = normalize_text(message)
        if not norm_msg:
            return {choice.name: 0.0 for choice in self.choices}

        query_vec = self.vectorizer.transform([norm_msg])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]

        scores: Dict[str, float] = {choice.name: 0.0 for choice in self.choices}
        for idx, sim in enumerate(similarities):
            label = self._corpus_labels[idx]
            if sim > scores[label]:
                scores[label] = float(sim)

        return scores

    def classify(self, message: str) -> ClassificationResult:
        """
        Classifies input message and returns predicted Intent with calibrated confidence.
        """
        norm_msg = normalize_text(message)
        raw_scores = self._calculate_scores(message)
        
        # Handle empty/unmatched inputs
        if all(score == 0.0 for score in raw_scores.values()) or not norm_msg:
            return ClassificationResult(
                intent=Intent.SUPPORT,
                confidence=0.30,
                scores=raw_scores
            )

        # Check explicitly ambiguous / generic prompts
        raw_clean = message.lower().strip()
        for pattern in AMBIGUOUS_PATTERNS:
            if re.match(pattern, raw_clean):
                best_intent_name = max(raw_scores, key=raw_scores.get)
                return ClassificationResult(
                    intent=Intent(best_intent_name),
                    confidence=0.45,
                    scores={k: round(v, 4) for k, v in raw_scores.items()}
                )

        # Sort intents by similarity score
        sorted_intents = sorted(raw_scores.items(), key=lambda item: item[1], reverse=True)
        best_intent_name, top_score = sorted_intents[0]
        second_score = sorted_intents[1][1] if len(sorted_intents) > 1 else 0.0
        margin = top_score - second_score

        # Calibrate confidence:
        if top_score < 0.20:
            confidence = max(0.35, top_score * 1.5)
        else:
            base_conf = 0.70 + (top_score * 0.25)
            if margin >= 0.15 or second_score == 0.0:
                confidence = min(0.98, base_conf + 0.05)
            elif margin < 0.05:
                confidence = max(0.40, base_conf - 0.25)
            else:
                confidence = min(0.90, base_conf)

        confidence = round(float(np.clip(confidence, 0.0, 1.0)), 2)

        return ClassificationResult(
            intent=Intent(best_intent_name),
            confidence=confidence,
            scores={k: round(v, 4) for k, v in raw_scores.items()}
        )

    def explain(self, message: str) -> Dict[str, Any]:
        """
        Debug utility displaying detailed similarity distributions and calculation steps.
        """
        result = self.classify(message)
        explanation = {
            "input": message,
            "normalized_input": normalize_text(message),
            "intent_scores": result.scores,
            "selected_intent": result.intent.value,
            "confidence": result.confidence,
            "threshold": self.confidence_threshold,
            "passes_threshold": result.confidence >= self.confidence_threshold
        }
        return explanation


# Default global classifier instance for LangGraph nodes
default_classifier = JevCompatibleClassifier()


def jev_router(state: MerchantState) -> MerchantState:
    """
    LangGraph node: Classifies user message using the local Jev-compatible classifier.
    Stores predicted intent and confidence into MerchantState.
    Strictly isolated: does not perform any business calculations.
    """
    result = default_classifier.classify(state.message)
    state.intent = result.intent
    state.confidence = result.confidence
    return state
