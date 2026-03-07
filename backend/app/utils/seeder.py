from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from ..models import UserProfile
from ..repositories import UserRepository, UserProfileRepository
from ..utils.enums import UserAgeGroupEnum, UserDrivingStyleEnum, UserGenderEnum
from ..utils.security import get_password_hash


class DatabaseSeeder:
	DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "example_users.json"

	@staticmethod
	def load_seed_data(file_path: Path | None = None) -> list[dict[str, Any]]:
		source_path = file_path or DatabaseSeeder.DATA_FILE
		if not source_path.exists():
			raise FileNotFoundError(f"Seed data file not found: {source_path}")

		payload = json.loads(source_path.read_text(encoding="utf-8"))
		return payload.get("users", [])

	@staticmethod
	def build_profile_data(profile_payload: dict[str, Any], user_id: int) -> dict[str, Any]:
		return {
			"user_id": user_id,
			"gender_identity": UserGenderEnum(profile_payload["gender"]),
			"age_group": UserAgeGroupEnum(profile_payload["age_group"]),
			"driving_experience_years": int(profile_payload["driving_experience_years"]),
			"driving_style": UserDrivingStyleEnum(profile_payload["driving_style"]),
			"gender_self_description": profile_payload.get("gender_self_description"),
		}

	@staticmethod
	def seed_users(db: Session, file_path: Path | None = None) -> dict[str, int]:
		users_payload = DatabaseSeeder.load_seed_data(file_path)
		user_repo = UserRepository(db)
		profile_repo = UserProfileRepository(db)

		created_users = 0
		created_profiles = 0
		skipped_users = 0

		for item in users_payload:
			email = item["email"]
			existing_user = user_repo.get_by_email(email)

			if existing_user is None:
				existing_user = user_repo.create(
					{
						"name": item["name"],
						"surname": item["surname"],
						"email": email,
						"password_hash": get_password_hash(item["password"]),
					}
				)
				created_users += 1
			else:
				skipped_users += 1

			existing_profile = (
				profile_repo.db.query(UserProfile)
				.filter(UserProfile.user_id == existing_user.id)
				.first()
			)

			profile_payload = item.get("profile")
			if profile_payload and existing_profile is None:
				profile_repo.create(
					DatabaseSeeder.build_profile_data(
						profile_payload=profile_payload,
						user_id=existing_user.id,
					)
				)
				created_profiles += 1

		return {
			"total_input": len(users_payload),
			"created_users": created_users,
			"created_profiles": created_profiles,
			"skipped_users": skipped_users,
		}
