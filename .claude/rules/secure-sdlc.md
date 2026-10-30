<!-- Generated from ottuco/governance RUL-SD-003 version 1.0 (commit 021184a). Do not edit here: change the standard. -->

# Secure SDLC review rules

## Every repository

#### Input and output
- Validate every input on the server: type, length, format and allowed values. Checks in the browser or app are a convenience, not a control. [6.2.4, A.8.28]
- Build database queries with the ORM or bound parameters. Never put user input into SQL, shell commands, file paths or templates by string formatting. [6.2.4, A.8.28]
- Never run user input as code: no eval or exec on it, no unpickling or unsafe YAML loading of it, no shell=True with it. [6.2.4, A.8.28]
- Escape output for where it lands: HTML, attribute, URL or JavaScript. Never mark user-supplied content as safe. [6.2.4, A.8.28]
- Error responses never show stack traces, queries, internal hostnames or configuration. [6.2.4, A.8.28]
#### Access control
- Every endpoint, mutation, view and download checks on the server who is asking and whether they may act on that object. Changing an id in a request must never reach another merchant's or customer's data (IDOR). [6.2.4, A.8.28]
- A new endpoint is closed by default, and access is granted explicitly. Hiding a button is not access control. [6.2.4, A.8.28]
- Sessions and tokens expire, end on logout, and never travel in URLs. [6.2.4, A.8.28]
#### Secrets and data
- No secret, key, token or password in code, configuration files, fixtures, tests or logs. Read them from the secret store or the environment. [6.2.4, A.8.28]
- Never log card data (full card number, CVV, PIN, track data), passwords, keys or tokens. Mask or tokenize personal data before it is logged. [6.2.4, A.8.28]
- No real customer data or real card numbers in fixtures, tests, seed data, the sandbox or staging. [6.5.5, A.8.33]
- Test accounts, test data and debug switches are removed before release. [6.5.6, A.8.33]
#### Cryptography
- Use the platform's cryptography libraries and current algorithms, never your own. No MD5 or SHA-1 for security, and never turn off certificate verification. [6.2.4, A.8.28]
- Compare tokens, signatures and other secrets in constant time. [6.2.4, A.8.28]
#### Payments and business logic
- Amounts, currencies, states and limits come from stored server-side data, never from the request. [6.2.4, A.8.28]
- Anything that moves money is idempotent and safe against replay and double submission. [6.2.4, A.8.28]
- Webhooks and callbacks are acted on only after the sender's signature is verified, or the result is confirmed with the gateway (an inquiry). [6.2.4, A.8.28]
- Outbound requests verify TLS, set a timeout and go only to known destinations. Never fetch a URL taken from user input (SSRF). [6.2.4, A.8.28]
#### Dependencies and change
- A new dependency arrives through the lockfile, with its reason in the pull request, an allowed license and no known critical or high vulnerability. [6.3.2, 6.3.3, A.8.8]
- Do not merge with a security-gate finding open. Fix it, or write on the pull request why it is accepted. [6.2.3, A.8.29]
- Open a pull request as a draft while the work goes on, and mark it ready for review when it is complete and tested: the checks run on ready pull requests. [6.5.1, A.8.32]
- A coding agent works only through its owner's own agent account: it never approves a pull request and never changes the build pipeline, and its owner is the author who answers for its code. [6.2.3, A.5.3, A.8.32]
- The pull request names its ticket, its security impact and how to roll it back. [6.5.1, A.8.32]
- A change marked significant does not merge until a security reviewer has approved its pre-release security review. [6.5.1, A.8.26]
- Changes to sign-in, permissions, cryptography, payment flows or outside connections are reviewed by someone trained in secure coding. [6.2.3.1, A.8.28]

## Python

- Keep Django's CSRF protection on. csrf_exempt is only for gateway and server-to-server callbacks, which verify a signature or confirm the result with the gateway first. [6.2.4, A.8.28]
- Never pass a formatted string to raw(), extra() or cursor.execute(); pass parameters. [6.2.4, A.8.28]
- Never use mark_safe or the safe filter on anything a user supplied. [6.2.4, A.8.28]
- Every DRF view and GraphQL resolver sets its permission check explicitly and scopes its queryset to the requesting merchant. [6.2.4, A.8.28]
- yaml.safe_load, never yaml.load. Never unpickle data from outside the process. [6.2.4, A.8.28]
- subprocess takes a list of arguments. Never shell=True with input in the command. [6.2.4, A.8.28]
- Every requests or httpx call sets a timeout, and never verify=False. [6.2.4, A.8.28]
- Generate tokens with the secrets module, and compare them with hmac.compare_digest. [6.2.4, A.8.28]
- Production settings: DEBUG off, ALLOWED_HOSTS set, the session cookie Secure, HttpOnly and SameSite, and the CSRF cookie Secure. [6.2.4, A.8.28]
