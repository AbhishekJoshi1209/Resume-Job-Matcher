import torch  # Must be imported first on Windows to fix DLL load order (WinError 1114)
import argparse
from src.matcher import ResumeMatcher
from src.utils import read_file, format_report

def main():
    parser = argparse.ArgumentParser(
        description="Resume-Job Matching System"
    )
    
    parser.add_argument(
        'resume',
        help='Path to resume file (txt or pdf)'
    )
    parser.add_argument(
        'job_description',
        help='Path to job description file'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    
    args = parser.parse_args()
    
    # Read files
    resume_text = read_file(args.resume)
    job_text = read_file(args.job_description)
    
    # Perform matching
    matcher = ResumeMatcher()
    result = matcher.match_resume_to_job(resume_text, job_text)
    
    # Display results
    if args.json:
        import json
        print(json.dumps(result, indent=2))
    else:
        print(format_report(result))

if __name__ == "__main__":
    main()