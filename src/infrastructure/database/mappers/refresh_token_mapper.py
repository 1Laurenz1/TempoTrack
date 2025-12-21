from src.domain.entities.refresh_token import RefreshToken
from src.infrastructure.database.models.refresh_token import RefreshTokenModel

class RefreshTokenMapper:
    @staticmethod
    def to_orm(refresh_token: RefreshToken) -> RefreshTokenModel:
        return RefreshTokenModel(
            id=refresh_token.id,
            user_id=refresh_token.user_id,
            token_hash=refresh_token.token_hash.encode() if isinstance(refresh_token.token_hash, str) else refresh_token.token_hash,
            revoked=refresh_token.revoked,
            expires_at=refresh_token.expires_at,
            created_at=refresh_token.created_at,
            updated_at=refresh_token.updated_at,
        )

    @staticmethod
    def to_domain(refresh_token_model: RefreshTokenModel) -> RefreshToken:
        return RefreshToken(
            id=refresh_token_model.id,
            user_id=refresh_token_model.user_id,
            token_hash=refresh_token_model.token_hash.decode() if isinstance(refresh_token_model.token_hash, bytes) else refresh_token_model.token_hash,
            revoked=refresh_token_model.revoked,
            expires_at=refresh_token_model.expires_at,
            created_at=refresh_token_model.created_at,
            updated_at=refresh_token_model.updated_at,
        )
