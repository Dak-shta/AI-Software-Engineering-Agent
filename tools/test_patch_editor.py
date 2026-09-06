from tools.patch_editor import apply_patch


def test_patch():
    result = apply_patch(
        "sample_repo",
        "models.py",
        "self.email = email",
        "self.email = email"
    )

    print(result)


if __name__ == "__main__":
    test_patch()