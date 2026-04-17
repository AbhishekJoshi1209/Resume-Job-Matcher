def read_file(filepath: str) -> str:
    """Read text from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")

def format_report(result: dict) -> str:
    """Format matching result for display"""
    report = f"""
╔════════════════════════════════════════════════════════════════╗
║           RESUME-JOB MATCHING REPORT                           ║
╚════════════════════════════════════════════════════════════════╝

📊 OVERALL MATCH SCORE: {result['overall_match_score']}%

┌─ Score Breakdown ─────────────────────────────────────────────┐
│ Skills Match:       {result['skill_match_score']}% (40% weight)
│ Semantic Match:     {result['semantic_match_score']}% (35% weight)
│ Keywords Match:     {result['keyword_match_score']}% (25% weight)
└───────────────────────────────────────────────────────────────┘

✅ MATCHING SKILLS ({len(result['matching_skills'])}/{result['job_requirement_count']}):
{', '.join(result['matching_skills']) if result['matching_skills'] else 'None'}

❌ MISSING SKILLS ({len(result['missing_skills'])}/{result['job_requirement_count']}):
{', '.join(result['missing_skills']) if result['missing_skills'] else 'None - Perfect match!'}

📈 RESUME STATISTICS:
- Skills Found: {result['resume_skill_count']}
- Keywords Matched: {result['matching_keywords_count']}/{result['total_job_keywords']}
"""
    return report