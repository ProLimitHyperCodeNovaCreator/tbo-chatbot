import joblib
import numpy as np
from pathlib import Path
from datetime import datetime
from prisma import Prisma
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from app.features import featurize
from app.config import settings
from app.logger import setup_logger

logger = setup_logger(__name__)


async def train_model():
    """
    Train ML model with validation and metrics
    
    Returns:
        dict: Training metrics or None if training failed
    """
    db = Prisma()
    
    try:
        await db.connect()
        logger.info("Starting model training...")
        
        # Fetch training data
        rows = await db.training_events.find_many()
        logger.info(f"Loaded {len(rows)} training samples")
        
        if len(rows) < settings.min_training_samples:
            logger.warning(
                f"Insufficient training data: {len(rows)} samples "
                f"(minimum: {settings.min_training_samples})"
            )
            await db.disconnect()
            return None
        
        # Prepare features and labels
        X = np.array([featurize(r.__dict__) for r in rows])
        y = np.array([1 if r.accepted else 0 for r in rows])
        
        logger.info(f"Positive samples: {y.sum()}, Negative samples: {len(y) - y.sum()}")
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        model = LogisticRegression(
            max_iter=500,
            random_state=42,
            class_weight='balanced'  # Handle imbalanced data
        )
        model.fit(X_train, y_train)
        logger.info("Model training completed")
        
        # Evaluate
        y_pred = model.predict(X_test)
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1_score': f1_score(y_test, y_pred, zero_division=0),
            'training_samples': len(rows),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Model metrics: {metrics}")
        
        # Save model
        model_path = Path(settings.model_path)
        joblib.dump(model, model_path)
        logger.info(f"Model saved to {model_path}")
        
        # Save metrics
        metrics_path = model_path.with_suffix('.metrics.json')
        import json
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        await db.disconnect()
        return metrics
        
    except Exception as e:
        logger.error(f"Error during model training: {str(e)}", exc_info=True)
        try:
            await db.disconnect()
        except:
            pass
        return None
