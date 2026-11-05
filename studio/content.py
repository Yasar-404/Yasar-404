"""Everything the profile says. Edit this file to change the words, not the renderers."""

from __future__ import annotations

from dataclasses import dataclass

WORDMARK = "YASAR K"
HEADLINE = "FULL-STACK ENGINEER  ·  PRODUCT DESIGNER  ·  CHENNAI, IN"
TAGLINE = "From the first pixel to the last query."
STATUS = "OPEN TO FULL-STACK & SOFTWARE ENGINEERING ROLES"

LAYERS = (
    ("DESIGN", "Figma, Framer, design systems"),
    ("FRONTEND", "React, Next.js, TypeScript"),
    ("BACKEND", "Python, Java, Node.js, Go"),
    ("DATA", "SQL, PostgreSQL, data modelling"),
)

STACK = (
    ("FRONTEND", ("React", "Next.js", "TypeScript", "JavaScript", "Tailwind", "Motion")),
    ("BACKEND", ("Python", "Java", "Node.js", "Go", "REST APIs", "Prisma")),
    ("DATA & DELIVERY", ("SQL", "PostgreSQL", "Git", "GitHub Actions", "Vercel", "Netlify")),
    (
        "PRODUCT DESIGN",
        ("Figma", "Framer", "Webflow", "Illustrator", "Photoshop", "Design Systems"),
    ),
)


@dataclass(frozen=True)
class Project:
    slug: str
    title: str
    kind: str
    summary: tuple[str, str]
    tags: tuple[str, ...]


PROJECTS = (
    Project(
        "liftiq",
        "LiftIQ",
        "GYM MANAGEMENT SOFTWARE",
        (
            "Marketing site for gym software covering memberships,",
            "payments, attendance, leads and renewals.",
        ),
        ("NEXT.JS", "REACT 19", "TYPESCRIPT", "TAILWIND V4"),
    ),
    Project(
        "envguard",
        "EnvGuard",
        "SECURITY CLI  ·  ON PYPI",
        (
            "Finds exposed secrets in code and Git history with 16 rules,",
            "regex and Shannon entropy. Local-only, SARIF output, CI gate.",
        ),
        ("PYTHON", "ZERO RUNTIME DEPS", "PRE-COMMIT", "SARIF"),
    ),
    Project(
        "shortener",
        "URL Shortener",
        "BACKEND SERVICE",
        (
            "Standard-library Go service with a concurrency-safe store,",
            "random base62 keys, collision retries and graceful shutdown.",
        ),
        ("GO", "NET/HTTP", "SYNC.RWMUTEX", "LOG/SLOG"),
    ),
    Project(
        "walkin",
        "V4 Walk-in System",
        "CLIENT MANAGEMENT TOOL",
        (
            "Front-desk tool for a fitness centre: BMI, BMR and TDEE",
            "calculators, client history and printable PDF reports.",
        ),
        ("JAVASCRIPT", "JSPDF", "LOCAL STORAGE"),
    ),
)


@dataclass(frozen=True)
class Client:
    slug: str
    name: str
    industry: str
    summary: str
    tools: str
    motif: str
    url: str


CLIENTS = (
    Client(
        "cassinil",
        "Cassinil Engineers",
        "CONSTRUCTION & BUILDING APPROVALS",
        "Modern digital brand experience",
        "FIGMA  ·  FRAMER",
        "blueprint",
        "https://cassinil.in",
    ),
    Client(
        "v4",
        "V4 Fitness Hub",
        "FITNESS & REHABILITATION",
        "Responsive, SEO-focused gym website",
        "FIGMA  ·  HTML  ·  CSS  ·  JS",
        "pulse",
        "https://v4-fitness-hub.vercel.app",
    ),
    Client(
        "rune",
        "Rune Designs",
        "ARCHITECTURE & INTERIORS",
        "Minimal, gallery-style studio website",
        "FIGMA  ·  FRAMER",
        "gallery",
        "https://runedesigns.framer.website",
    ),
    Client(
        "aorganic",
        "A Organic Beauty Salon",
        "BEAUTY & SALON SERVICES",
        "Calm, nature-inspired wellness website",
        "FIGMA  ·  FRAMER",
        "bloom",
        "https://aorganicbeautysalon.framer.website",
    ),
)

# Reference snippets for the code panel: one renewals feature, across the stack.
SNIPPETS = (
    (
        "renewals.sql",
        "sql",
        """\
-- Memberships expiring soon, least recently seen first
WITH last_visit AS (
  SELECT member_id, MAX(checked_in_at) AS seen_at
  FROM attendance
  GROUP BY member_id
)
SELECT m.id, m.name, m.expires_on, v.seen_at,
       RANK() OVER (ORDER BY v.seen_at NULLS FIRST) AS churn_rank
FROM members m
LEFT JOIN last_visit v ON v.member_id = m.id
WHERE m.expires_on BETWEEN CURRENT_DATE AND CURRENT_DATE + 14
ORDER BY churn_rank;""",
    ),
    (
        "RenewalService.java",
        "java",
        """\
@Service
public class RenewalService {
    private final MemberRepository members;

    public RenewalService(MemberRepository members) {
        this.members = members;
    }

    @Transactional(readOnly = true)
    public List<RenewalDue> findDue(int withinDays) {
        LocalDate cutoff = LocalDate.now().plusDays(withinDays);
        return members.findExpiringBefore(cutoff).stream()
            .map(RenewalDue::from)
            .collect(Collectors.toList());
    }
}""",
    ),
    (
        "churn_risk.py",
        "python",
        '''\
from dataclasses import dataclass
from math import exp


@dataclass(frozen=True)
class Member:
    days_since_visit: int
    visits_last_90d: int
    tenure_months: int


def churn_risk(member: Member) -> float:
    """Logistic score in [0, 1]; higher means more likely to lapse."""
    z = 0.08 * member.days_since_visit - 0.05 * member.visits_last_90d
    return 1 / (1 + exp(-(z - 0.02 * member.tenure_months)))''',
    ),
    (
        "useRenewals.ts",
        "typescript",
        """\
export function useRenewals(withinDays = 14) {
  const [state, setState] = useState<State>({ status: "loading" });

  useEffect(() => {
    const controller = new AbortController();
    fetch(`/api/renewals?withinDays=${withinDays}`, { signal: controller.signal })
      .then((res) => res.json() as Promise<RenewalDue[]>)
      .then((rows) => setState({ status: "ready", rows }))
      .catch(() => {
        if (!controller.signal.aborted) setState({ status: "error" });
      });
    return () => controller.abort();
  }, [withinDays]);

  return state;
}""",
    ),
)
