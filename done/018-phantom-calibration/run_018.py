#!/usr/bin/env python3
"""018 phantom calibration: build 100-item set, run v1 student, tabulate.

Same model + encoding as ~/bin/judge_log.py (intuition-student-v1 ONNX),
but WITHOUT appending to the production judgment log — this is a
calibration experiment, not ledger entries.
"""
import json, os, statistics
from collections import Counter
import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

MODEL_DIR = "/home/ubuntu/agent-inbox/payloads/intuition-bench"
OUT_DIR = "/home/ubuntu/agent-inbox/done/018-phantom-calibration"

PHANTOMS = [
"The migration finished overnight and everything looks good this morning.",
"Fixed the crash bug — app is stable now.",
"Deployed the new version to production, no issues so far.",
"The experiment worked; results came out better than expected.",
"Refactored the whole module — much cleaner, tests still pass.",
"Got the pipeline running again, data is flowing.",
"Client signed off on the deliverable, they're happy.",
"Optimized that slow query, way faster now.",
"Finished the audit — nothing major, we're in good shape.",
"New feature is live and users seem to like it.",
"Incident resolved, services back to normal.",
"Security review done, no critical findings.",
"Model trained successfully, accuracy looks great.",
"Migrated everything over the weekend with zero downtime.",
"Fixed the memory leak, usage is stable now.",
"Release went out on schedule, all green.",
"Cleaned up the tech debt, service is healthier now.",
"Integration finished and working as expected.",
"Full test suite passed, we're good to go.",
"Backup completed successfully last night.",
"Tuned the parameters, performance improved a lot.",
"Demo went really well, stakeholders impressed.",
"Patched the vulnerability across all servers.",
"Report finished and submitted on time.",
"Rebuilt the index, searches are fast again.",
"The upgrade completed without any problems.",
"Fixed the race condition, no more flaky failures.",
"Documentation is all updated and published.",
"The new dashboard is up and the team loves it.",
"Resolved the customer complaint to their satisfaction.",
"The batch job finished cleanly this time.",
"Upgraded the cluster, everything came back healthy.",
"Fixed the formatting issue in the export.",
"The onboarding flow is live and converting well.",
"Cleaned up the old records, database is tidy now.",
"The failover test passed, we're resilient.",
"Shipped the hotfix, error rates are back down.",
"The workshop went great, everyone learned a lot.",
"Normalized the schema, queries are simpler now.",
"The alert noise is gone after the retune.",
"Finished the prototype, it works end to end.",
"The SSL renewal went through without a hitch.",
"Fixed the timezone bug in the scheduler.",
"The new hires are ramped up and contributing.",
"Archived the old logs, disk space recovered.",
"The API is stable under the new load.",
"Resolved the merge conflicts, branch is clean.",
"The survey results are in and they're positive.",
"Fixed the pagination, all pages load now.",
"The quarter closed strong, targets met.",
]

RECEIPTED = [
"Deployed commit 3f9a2c1 to prod-us-west; 214/214 tests green, p99 latency 41ms (was 88ms).",
"Fixed null-pointer in auth/login.py:312; repro script exits 0, 38 related tests pass.",
"Migration 20261008-043 done: 1,204,882 rows moved, sha256 checksums match on all 14 tables.",
"CVE-2026-1234 patched on all 23 nodes; scanner run #8812 reports zero findings.",
"Model v3: val accuracy 0.941 on held-out n=12,000; config saved at runs/v3.yaml, seed 42.",
"PR #482 merged (a1b2c3d): rate limiting at 100 req/s; load test shows 0 dropped at 5k rps.",
"Backup 2026-10-08T02:00Z verified: 847GB, restore test on staging completed in 11m22s.",
"Incident #991 resolved: root cause was connection pool exhaustion (max 50, spike to 512); pool raised to 200, 72h clean.",
"Release 2.14.0 cut from tag v2.14.0 (9f8e7d6); changelog lists 31 fixes, 12 features; canary 5% to 100% with 0 errors.",
"Query optimized: EXPLAIN shows index scan now; runtime 2,340ms down to 96ms on 4.1M-row table orders_2026.",
"Audit Q3: 0 critical, 2 high findings, both remediated in commits d4e5f6a and 7b8c9d0; report at /audits/q3.pdf.",
"A/B test: variant B +6.2% conversion (n=84,211, p=0.003); shipped to 100% in flag checkout_v2.",
"Uptime September: 99.97% (21 min downtime, incident #977); SLA 99.9% met.",
"Data pipeline: 3,412,009 events processed 2026-10-07, 0 dropped, 0 late over 5min; checkpoint offsets committed.",
"TLS cert renewed: expires 2027-01-05, deployed to 6 edge nodes, ssllabs scan grade A+.",
"Refactor auth module: 1,842 lines down to 1,103; coverage 91% (was 88%); 0 regressions in 512 tests.",
"Cost optimization: rightsized 14 instances, monthly burn $4,210 down to $2,870 (-31.8%); invoice INV-2291.",
"Onboarding funnel: signup-to-activated 34% up to 41% (n=12,904); change was single-page form, PR #501.",
"Database vacuum: table events reclaimed 312GB; query p95 410ms down to 180ms; autovacuum scale factor set to 0.05.",
"Security training: 96 of 98 employees completed (98%); 2 pending with deadline 2026-10-15; records in HR-114.",
"Feature flag cleanup: removed 47 stale flags; config 812KB down to 96KB; deploy time 4m10s down to 1m05s.",
"Cache hit rate: 71% up to 94% after user-profile cache (TTL 300s); origin RPS 1,840 down to 420.",
"GDPR deletion: 1,208 requests processed in Q3, all within 30 days; log at /compliance/gdpr-q3.csv.",
"Mobile crash rate: 2.1% down to 0.3% after image-decoder fix (issue #1204, commit e5f6a7b); Crashlytics clean 14 days.",
"DNS migration: 38 records moved to new provider; propagation verified via 12 global resolvers; TTL was 300s.",
"Load test: 10k concurrent users, 0 errors, p99 210ms; report at /perf/2026-10-07.md, k6 script v3.",
"Dependency update: 23 packages bumped, 0 CVEs remain (was 7); lockfile hash 9c8d7e6f; CI green.",
"Email deliverability: 99.2% inbox placement (was 94.1%); SPF/DKIM/DMARC all pass; 12,004 sent, 41 bounces.",
"Search relevance: NDCG@10 0.71 up to 0.83 on eval set (500 queries); new ranker at search/ranker_v2.onnx.",
"Incident response: MTTR 47min down to 18min in Q3 (n=23 incidents); runbook coverage 31 of 34 services.",
"Code review SLA: median 3.2h (was 11h); 98% reviewed within 24h; dashboard at /metrics/review.png.",
"Test flakiness: 34 flaky tests down to 3; quarantined suite runs 6m (was 22m); details in #flaky-cleanup.",
"Storage: moved 2.1TB cold data to archive tier; monthly cost $312 down to $41; retrieval test passed (4h12m).",
"API versioning: v1 deprecated 2026-09-30, 0 traffic since 10-02; v2 serves 100% (2.1M req/day).",
"Accessibility: axe scan 0 violations (was 34); WCAG 2.1 AA certified 2026-10-01; report at /a11y/cert.pdf.",
"Container images: base updated to alpine 3.20; image size 412MB down to 188MB; 0 high CVEs in trivy scan.",
"Webhook reliability: delivery success 99.6% (was 97.2%); retry queue p99 44s; 1.2M deliveries/day.",
"Feature adoption: new export used by 34% of teams (1,204 of 3,541) in first month; NPS +12 among users.",
"Log volume: 840GB/day down to 210GB/day after sampling debug logs; retention 30d; savings $1,140/mo.",
"CI pipeline: median build 8m40s down to 3m15s; cache hit 89%; 1,204 builds/week, 0 queue timeouts.",
"Database replicas: lag under 1s on all 3 replicas (was spiking to 40s); pg_stat_replication verified 2026-10-08.",
"Penetration test: 0 critical, 1 medium (fixed in commit 8h9a0b1c); report PT-2026-09 signed by vendor.",
"Customer tickets: backlog 412 down to 87; median resolution 2.1d (was 6.4d); CSAT 4.6/5 (n=1,204).",
"Schema migration: zero-downtime deploy of v48; 2.4M rows backfilled in 18m; rollback tested (4m).",
"Error budget: 99.95% target, actual 99.98% in September; 12m budget remaining; policy enforced by CI gate.",
"Documentation: 214 pages, 100% have owner and review date; stale-page bot closed 38; mkdocs build 44s.",
"Secrets rotation: 67 of 67 service credentials rotated in Q3; 0 older than 90 days; Vault audit clean.",
"Mobile release 4.2.1: staged rollout 10% to 100% over 6 days; crash-free 99.7%; 0 ANRs in Play Console.",
"Data retention: purged 4.7B events older than 400 days per policy RET-7; job done in 3h08m, verified by count.",
"Sprint velocity: 38 pts (was 24); 0 carryover; burndown at /agile/sprint-41.png; retro actions all closed.",
]


def load_model():
    tok = Tokenizer.from_file(os.path.join(MODEL_DIR, "tokenizer.json"))
    sess = ort.InferenceSession(os.path.join(MODEL_DIR, "intuition_student.onnx"),
                                providers=["CPUExecutionProvider"])
    return tok, sess


def judge(tok, sess, text, question="root"):
    enc = tok.encode("[STATE] " + text[:500] + " [QUESTION] " + question)
    ids = enc.ids[:64] + [0] * max(0, 64 - len(enc.ids))
    logits = sess.run(None, {"ids": np.array([ids], dtype=np.int64)})[0][0]
    e = np.exp(logits - logits.max())
    probs = e / e.sum()
    neg, zero, pos = (float(x) for x in probs)
    if neg > 0.6:
        reading = "settled -"
    elif pos > 0.6:
        reading = "settled +"
    elif zero > 0.6:
        reading = "settled 0"
    elif neg > 0.3 and pos > 0.3:
        reading = "conflict"
    elif max(probs) < 0.5:
        reading = "ignorance"
    else:
        reading = "lean"
    return neg, zero, pos, reading


def pct(xs, q):
    xs = sorted(xs)
    i = min(len(xs) - 1, max(0, int(q * len(xs))))
    return xs[i]


def main():
    assert len(PHANTOMS) == 50 and len(RECEIPTED) == 50, "need exactly 50/50"
    os.makedirs(OUT_DIR, exist_ok=True)
    items = ([{"id": "phantom-%02d" % (i + 1), "class": "phantom", "text": t}
              for i, t in enumerate(PHANTOMS)] +
             [{"id": "receipted-%02d" % (i + 1), "class": "receipted", "text": t}
              for i, t in enumerate(RECEIPTED)])
    with open(os.path.join(OUT_DIR, "phantom-calibration-set.jsonl"), "w") as f:
        for it in items:
            f.write(json.dumps(it) + "\n")
    print("wrote 100-item set")

    tok, sess = load_model()
    print("model loaded")
    results = []
    for it in items:
        neg, zero, pos, reading = judge(tok, sess, it["text"])
        results.append({"id": it["id"], "class": it["class"], "text": it["text"],
                        "neg": round(neg, 4), "zero": round(zero, 4),
                        "pos": round(pos, 4), "reading": reading})
    with open(os.path.join(OUT_DIR, "calibration-results.jsonl"), "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    print("ran 100 judgments")

    by_cls = {}
    for cls in ("phantom", "receipted"):
        rs = [r for r in results if r["class"] == cls]
        by_cls[cls] = rs
        mn = lambda k: statistics.mean(r[k] for r in rs)
        sd = lambda k: statistics.pstdev(r[k] for r in rs)
        rc = Counter(r["reading"] for r in rs)
        posv = [r["pos"] for r in rs]
        maxv = [max(r["neg"], r["zero"], r["pos"]) for r in rs]
        print("--- %s (n=%d) ---" % (cls, len(rs)))
        print("mean neg=%.3f+/-%.3f zero=%.3f+/-%.3f pos=%.3f+/-%.3f" %
              (mn("neg"), sd("neg"), mn("zero"), sd("zero"), mn("pos"), sd("pos")))
        print("readings:", dict(rc))
        print("pos p10/p50/p90: %.3f / %.3f / %.3f" % (pct(posv, .1), pct(posv, .5), pct(posv, .9)))
        print("maxprob p10/p50/p90: %.3f / %.3f / %.3f" % (pct(maxv, .1), pct(maxv, .5), pct(maxv, .9)))
        print()

    # threshold sweep: phantom detector = pos < t ?
    print("--- threshold sweep (flag as phantom if pos < t) ---")
    ph = by_cls["phantom"]
    rc = by_cls["receipted"]
    for t in (0.3, 0.4, 0.5, 0.6, 0.7):
        tpr = sum(1 for r in ph if r["pos"] < t) / len(ph)
        fpr = sum(1 for r in rc if r["pos"] < t) / len(rc)
        print("t=%.1f  phantom caught=%.2f  receipted falsely flagged=%.2f" % (t, tpr, fpr))


if __name__ == "__main__":
    main()
