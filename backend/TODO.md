# TODO

## Auth/register password hashing failures (passlib[bcrypt] / bcrypt)

- [ ] Fix password hashing implementation to avoid bcrypt/passlib crashing and bcrypt 72-byte limit.
- [ ] Pin compatible bcrypt version in dependencies.
- [ ] Re-test `/auth/register` with normal + long passwords.

