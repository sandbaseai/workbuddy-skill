import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SiteDataTests(unittest.TestCase):
    def test_curated_adaptations_are_installable_and_workbuddy_ready(self):
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_site_data.py")],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        records = json.loads((ROOT / "site" / "catalog.json").read_text(encoding="utf-8"))
        cache_engineering = next(
            item
            for item in records
            if item["r"] == "Dankosik/go-service-template-rest"
            and item["p"]
            == "docs/universal-disciplines/cache-engineering/SKILL.md"
        )
        self.assertEqual(cache_engineering["w"], "workbuddy-ready")
        self.assertEqual(cache_engineering["g"], "development")
        self.assertTrue(
            cache_engineering["a"].endswith(
                "/cache-engineering-workbuddy-skill.zip"
            )
        )
        container_image = next(
            item
            for item in records
            if item["r"] == "codewithmukesh/dotnet-claude-kit"
            and item["p"] == "skills/docker/SKILL.md"
        )
        self.assertEqual(container_image["w"], "workbuddy-ready")
        self.assertEqual(container_image["g"], "development")
        self.assertTrue(
            container_image["a"].endswith(
                "/container-image-engineering-workbuddy-skill.zip"
            )
        )
        kubernetes = next(
            item
            for item in records
            if item["r"] == "LukasNiessen/kubernetes-skill"
            and item["p"] == "SKILL.md"
        )
        self.assertEqual(kubernetes["w"], "workbuddy-ready")
        self.assertEqual(kubernetes["g"], "development")
        self.assertTrue(
            kubernetes["a"].endswith("/kubernetes-operations-workbuddy-skill.zip")
        )
        terraform = next(
            item
            for item in records
            if item["r"] == "antonbabenko/terraform-skill"
            and item["p"] == "skills/terraform-skill/SKILL.md"
        )
        self.assertEqual(terraform["w"], "workbuddy-ready")
        self.assertEqual(terraform["g"], "development")
        self.assertTrue(
            terraform["a"].endswith("/terraform-engineering-workbuddy-skill.zip")
        )
        postgres = next(
            item
            for item in records
            if item["r"] == "supabase/agent-skills"
            and item["p"] == "skills/supabase-postgres-best-practices/SKILL.md"
        )
        self.assertEqual(postgres["w"], "workbuddy-ready")
        self.assertEqual(postgres["g"], "data")
        self.assertTrue(
            postgres["a"].endswith("/postgres-engineering-workbuddy-skill.zip")
        )
        oauth = next(
            item
            for item in records
            if item["r"] == "ssrjkk/claude-skills"
            and item["p"] == ".claude/skills/security/oauth-debugging/SKILL.md"
        )
        self.assertEqual(oauth["w"], "workbuddy-ready")
        self.assertEqual(oauth["g"], "security")
        self.assertTrue(oauth["a"].endswith("/oauth-debugging-workbuddy-skill.zip"))
        graphql = next(
            item
            for item in records
            if item["r"] == "FutureJJ/claude-skills"
            and item["p"] == "skills/graphql-expert/SKILL.md"
        )
        self.assertEqual(graphql["w"], "workbuddy-ready")
        self.assertEqual(graphql["g"], "development")
        self.assertTrue(graphql["a"].endswith("/graphql-expert-workbuddy-skill.zip"))
        observability = next(
            item
            for item in records
            if item["r"] == "FutureJJ/claude-skills"
            and item["p"] == "skills/monitoring-observability/SKILL.md"
        )
        self.assertEqual(observability["w"], "workbuddy-ready")
        self.assertEqual(observability["g"], "development")
        self.assertTrue(
            observability["a"].endswith(
                "/monitoring-observability-workbuddy-skill.zip"
            )
        )
        mysql = next(
            item
            for item in records
            if item["r"] == "ssrjkk/claude-skills"
            and item["p"] == ".claude/skills/database/mysql/SKILL.md"
        )
        self.assertEqual(mysql["w"], "workbuddy-ready")
        self.assertEqual(mysql["g"], "data")
        self.assertTrue(mysql["a"].endswith("/mysql-workbuddy-skill.zip"))
        data_analysis = next(
            item
            for item in records
            if item["r"] == "datar-gaurav/sutra-os"
            and item["p"] == "backend/skills/data-analysis/SKILL.md"
        )
        self.assertEqual(data_analysis["w"], "workbuddy-ready")
        self.assertEqual(data_analysis["g"], "data")
        self.assertTrue(data_analysis["a"].endswith("/data-analysis-workbuddy-skill.zip"))
        privacy = next(
            item
            for item in records
            if item["r"] == "rocklambros/rcs"
            and item["p"] == "skills/ml-datasci/applying-differential-privacy/SKILL.md"
        )
        self.assertEqual(privacy["w"], "workbuddy-ready")
        self.assertEqual(privacy["g"], "data")
        self.assertTrue(
            privacy["a"].endswith("/differential-privacy-workbuddy-skill.zip")
        )
        openapi = next(
            item
            for item in records
            if item["r"] == "majiayu000/claude-skill-registry"
            and item["p"] == "skills/quality/validate-openapi-spec/SKILL.md"
        )
        self.assertEqual(openapi["w"], "workbuddy-ready")
        self.assertEqual(openapi["g"], "development")
        self.assertTrue(openapi["a"].endswith("/openapi-review-workbuddy-skill.zip"))
        security_review = next(
            item
            for item in records
            if item["r"] == "aydabd/github-bootstrap"
            and item["p"] == "templates/.github/skills/security-review/SKILL.md"
        )
        self.assertEqual(security_review["w"], "workbuddy-ready")
        self.assertEqual(security_review["g"], "security")
        self.assertTrue(
            security_review["a"].endswith("/security-review-workbuddy-skill.zip")
        )
        threat_model = next(
            item
            for item in records
            if item["r"] == "phamhungptithcm/ai-agent-kit"
            and item["p"]
            == "assets/enterprise-ai-agent-os/.ai/skills-src/threat-model/SKILL.md"
        )
        self.assertEqual(threat_model["w"], "workbuddy-ready")
        self.assertEqual(threat_model["g"], "security")
        self.assertTrue(threat_model["a"].endswith("/threat-model-workbuddy-skill.zip"))
        synthesis = next(
            item
            for item in records
            if item["r"] == "itseffi/productize"
            and item["p"]
            == "skills/productize-fragmented-user-research-synthesis-into-coherent-insights/SKILL.md"
        )
        self.assertEqual(synthesis["w"], "workbuddy-ready")
        self.assertEqual(synthesis["g"], "research")
        self.assertTrue(
            synthesis["a"].endswith("/user-research-synthesis-workbuddy-skill.zip")
        )
        roadmap = next(
            item
            for item in records
            if item["r"] == "davidvictor/adlc-skills"
            and item["p"] == "skills/adlc/adlc-roadmap/SKILL.md"
        )
        self.assertEqual(roadmap["w"], "workbuddy-ready")
        self.assertEqual(roadmap["g"], "business")
        self.assertTrue(roadmap["a"].endswith("/product-roadmap-workbuddy-skill.zip"))
        migration = next(
            item
            for item in records
            if item["r"] == "Kushagrabainsla/north"
            and item["p"] == "skills/builtin/data-and-schema-migration/SKILL.md"
        )
        self.assertEqual(migration["w"], "workbuddy-ready")
        self.assertEqual(migration["g"], "data")
        self.assertTrue(
            migration["a"].endswith("/data-and-schema-migration-workbuddy-skill.zip")
        )
        pre_mortem = next(
            item
            for item in records
            if item["r"] == "charly-vibes/wai"
            and item["p"] == ".claude/skills/pre-mortem/SKILL.md"
        )
        self.assertEqual(pre_mortem["w"], "workbuddy-ready")
        self.assertEqual(pre_mortem["g"], "business")
        self.assertTrue(pre_mortem["a"].endswith("/pre-mortem-workbuddy-skill.zip"))
        architecture = next(
            item
            for item in records
            if item["r"] == "placerda/agentic-engineering"
            and item["p"] == ".github/skills/architecture-decision/SKILL.md"
        )
        self.assertEqual(architecture["w"], "workbuddy-ready")
        self.assertEqual(architecture["g"], "development")
        self.assertTrue(
            architecture["a"].endswith("/architecture-decision-workbuddy-skill.zip")
        )
        incident = next(
            item
            for item in records
            if item["r"] == "jukrap/ai-agent-playbook"
            and item["p"] == "skills/devops/observability-incident-triage/SKILL.md"
        )
        self.assertEqual(incident["w"], "workbuddy-ready")
        self.assertEqual(incident["g"], "security")
        self.assertTrue(incident["a"].endswith("/incident-triage-workbuddy-skill.zip"))
        debugging = next(
            item
            for item in records
            if item["r"] == "GuicedEE/ai-rules"
            and item["p"] == "skills/.curated/systematic-debugging/SKILL.md"
        )
        self.assertEqual(debugging["w"], "workbuddy-ready")
        self.assertEqual(
            debugging["a"],
            "https://github.com/sandbaseai/workbuddy-skill/releases/latest/download/"
            "systematic-debugging-workbuddy-skill.zip",
        )
        spreadsheet = next(
            item
            for item in records
            if item["r"] == "xuthreekid/clawchain"
            and item["p"] == "backend/data/skills/excel-ops/SKILL.md"
        )
        self.assertEqual(spreadsheet["w"], "workbuddy-ready")
        self.assertEqual(spreadsheet["g"], "data")
        self.assertTrue(spreadsheet["a"].endswith("/excel-ops-workbuddy-skill.zip"))
        dense_writing = next(
            item
            for item in records
            if item["r"] == "Bogyie/llm-reliability-skill"
            and item["p"] == "skills/dense-writing/SKILL.md"
        )
        self.assertEqual(dense_writing["w"], "workbuddy-ready")
        self.assertEqual(dense_writing["g"], "content")
        self.assertTrue(dense_writing["a"].endswith("/dense-writing-workbuddy-skill.zip"))
        accessibility = next(
            item
            for item in records
            if item["r"] == "joaocarloscruz/skills"
            and item["p"] == "library/review-accessibility/SKILL.md"
        )
        self.assertEqual(accessibility["w"], "workbuddy-ready")
        self.assertEqual(accessibility["g"], "design")
        self.assertTrue(
            accessibility["a"].endswith("/review-accessibility-workbuddy-skill.zip")
        )
        test_strategy = next(
            item
            for item in records
            if item["r"] == "joaocarloscruz/skills"
            and item["p"] == "library/design-test-strategy/SKILL.md"
        )
        self.assertEqual(test_strategy["w"], "workbuddy-ready")
        self.assertEqual(test_strategy["g"], "development")
        self.assertTrue(
            test_strategy["a"].endswith("/design-test-strategy-workbuddy-skill.zip")
        )
        handoff = next(
            item
            for item in records
            if item["r"] == "quarcs-lab/project20XXy"
            and item["p"] == ".claude/skills/handoff/SKILL.md"
        )
        self.assertEqual(handoff["w"], "workbuddy-ready")
        self.assertEqual(handoff["g"], "productivity")
        self.assertTrue(handoff["a"].endswith("/handoff-workbuddy-skill.zip"))
        performance = next(
            item
            for item in records
            if item["r"] == "joaocarloscruz/skills"
            and item["p"] == "library/improve-performance/SKILL.md"
        )
        self.assertEqual(performance["w"], "workbuddy-ready")
        self.assertEqual(performance["g"], "development")
        self.assertTrue(
            performance["a"].endswith("/improve-performance-workbuddy-skill.zip")
        )
        cli = next(
            item
            for item in records
            if item["r"] == "joaocarloscruz/skills"
            and item["p"] == "library/test-cli/SKILL.md"
        )
        self.assertEqual(cli["w"], "workbuddy-ready")
        self.assertEqual(cli["g"], "development")
        self.assertTrue(cli["a"].endswith("/test-cli-workbuddy-skill.zip"))
        meeting = next(
            item
            for item in records
            if item["r"] == "rainoff/skill-gauge"
            and item["p"]
            == "exercises/fixtures/meeting-notes/skill/meeting-notes/SKILL.md"
        )
        self.assertEqual(meeting["w"], "workbuddy-ready")
        self.assertEqual(meeting["g"], "productivity")
        self.assertTrue(meeting["a"].endswith("/meeting-notes-workbuddy-skill.zip"))
        release = next(
            item
            for item in records
            if item["r"] == "joaocarloscruz/skills"
            and item["p"] == "library/release-software/SKILL.md"
        )
        self.assertEqual(release["w"], "workbuddy-ready")
        self.assertEqual(release["g"], "development")
        self.assertTrue(release["a"].endswith("/release-software-workbuddy-skill.zip"))
        research = next(
            item
            for item in records
            if item["r"] == "Animism001/skills"
            and item["p"] == ".agents/skills/web-researcher/SKILL.md"
        )
        self.assertEqual(research["w"], "workbuddy-ready")
        self.assertEqual(research["g"], "research")
        self.assertTrue(research["a"].endswith("/web-researcher-workbuddy-skill.zip"))
        email = next(
            item
            for item in records
            if item["r"] == "datar-gaurav/sutra-os"
            and item["p"] == "backend/skills/email-drafting/SKILL.md"
        )
        self.assertEqual(email["w"], "workbuddy-ready")
        self.assertEqual(email["g"], "business")
        self.assertTrue(email["a"].endswith("/email-drafting-workbuddy-skill.zip"))
        requirements = next(
            item
            for item in records
            if item["r"] == "l-gevity/l-gevity-skills"
            and item["p"] == ".agents/skills/requirements-grounding/SKILL.md"
        )
        self.assertEqual(requirements["w"], "workbuddy-ready")
        self.assertEqual(requirements["g"], "business")
        self.assertTrue(
            requirements["a"].endswith("/requirements-grounding-workbuddy-skill.zip")
        )
        prioritization = next(
            item
            for item in records
            if item["r"] == "henrique-simoes/Istara"
            and item["p"] == "skills/define/prioritization-matrix/SKILL.md"
        )
        self.assertEqual(prioritization["w"], "workbuddy-ready")
        self.assertEqual(prioritization["g"], "business")
        self.assertTrue(
            prioritization["a"].endswith("/prioritization-matrix-workbuddy-skill.zip")
        )
        metadata = json.loads(
            (ROOT / "site" / "catalog-meta.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            metadata["curated_adaptations"],
            len(json.loads((ROOT / "catalog/curated.json").read_text(encoding="utf-8"))),
        )


if __name__ == "__main__":
    unittest.main()
