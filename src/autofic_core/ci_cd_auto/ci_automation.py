import subprocess

class Ci_Automate:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.REPO_URLS = [
            'https://github.com/inyeongjang/corner4',
            'https://github.com/markedjs/marked',
            'https://github.com/validatorjs/validator.js',
            'https://github.com/vercel/serve',
            'https://github.com/http-party/http-server',
            'https://github.com/expressjs/express',
        ]
    def run_autofic(self):
        print(f"\n[RUN] {self.repo_url}")
        cmd = [
            'python', '-m', 'autofic_core.cli',
            '--repo', self.repo_url,
            '--save-dir', 'downloaded_folder',
            '--sast',
            '--rule', 'p/javascript'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return

    def main(self):
        for self.repo_url in self.REPO_URLS:
            try:
                self.run_autofic(self.repo_url)
            except Exception as e:
                print(f"[ERROR] {self.repo_url}: {e}")

if __name__ == "__main__":
    Ci_Automate().main()
