import os
from .create_yml import AboutYml
from .env_encrypt import EnvEncrypy
from .pr_procedure import PRProcedure

# GitHub PR 자동화 클래스
class BranchPRAutomation:
    def __init__(self, repo_url: str, save_dir: str):
        self.result = {
            "post_init": False,
            "mv_workdir": False,
            "check_branch": False,
            "discordwebhook": False,
            "slackwebhook": False,
            "create_yml": False,
            "push_yml": False,
            "change_files": False,
            "get_main_branch": False,
            "generate_pr": False,
            "create_upstream_pr": False,
            "error_msg": None,
        }
        # 브랜치 숫자
        self.branch_num = 1
        # 기본 브랜치는 main으로 설정
        self.base_branch = 'main'
        # 원본 레포, 레포 이름 초기값 선언
        self.repo_name = "UNKOWN"
        self.upstream_owner = "UNKOWN"
        # repo_url은 GitHub 저장소 URL이어야 함
        self.save_dir = save_dir + '/repo'
        self.repo_url = repo_url.rstrip('/').rstrip('.git')
        # Discord, Slack을 Github랑 연결하려면, 아래 변수를 추가해야함
        self.secret_discord = 'DISCORD_WEBHOOK_URL'
        self.secret_slack = "SLACK_WEBHOOK_URL"
        # .env 파일에서 환경 변수 로드
        self.token = os.getenv('GITHUB_TOKEN')
        self.user_name = os.getenv('USER_NAME')
        self.slack_webhook = os.environ.get('SLACK_WEBHOOK_URL')
        self.discord_webhook = os.environ.get('DISCORD_WEBHOOK_URL')

    def run(self):
        pr_procedure = PRProcedure(self.branch_num, self.base_branch, self.repo_name,
                                   self.upstream_owner, self.save_dir, self.repo_url,
                                   self.secret_discord, self.secret_slack, self.token,
                                   self.user_name, self.slack_webhook, self.discord_webhook)

        # 1. 사용자 이름 확인
        try:
            pr_procedure.post_init()
            self.result["post_init"] = True
        except Exception as e:
            self.result["error_msg"] = f"post_init: {e}"
            return self.result

        # 2. 작업 디렉토리 이동
        try:
            pr_procedure.mv_workdir()
            self.result["mv_workdir"] = True
        except Exception as e:
            self.result["error_msg"] = f"mv_workdir: {e}"
            return self.result

        # 3. 브랜치 확인/생성
        try:
            pr_procedure.check_branch_exists()
            self.result["check_branch"] = True
        except Exception as e:
            self.result["error_msg"] = f"check_branch: {e}"
            return self.result

        # 4. Discord Webhook
        try:
            EnvEncrypy(self.user_name, self.repo_name, self.token).discordwebhook_notifier(self.secret_discord)
            self.result["discordwebhook"] = True
        except Exception as e:
            self.result["error_msg"] = f"discordwebhook: {e}"
            return self.result

        # 5. Slack Webhook
        try:
            EnvEncrypy(self.user_name, self.repo_name, self.token).slackwebhook_notifier(self.secret_slack)
            self.result["slackwebhook"] = True
        except Exception as e:
            self.result["error_msg"] = f"slackwebhook: {e}"
            return self.result

        # 6. pr_notify.yml 파일 생성
        try:
            AboutYml().create_pr_yml()
            self.result["create_yml"] = True
        except Exception as e:
            self.result["error_msg"] = f"create_yml: {e}"
            return self.result

        # 7. pr_notify.yml push
        try:
            AboutYml().push_pr_yml(self.user_name, self.repo_name, self.token, self.branch_name)
            self.result["push_yml"] = True
        except Exception as e:
            self.result["error_msg"] = f"push_yml: {e}"
            return self.result

        # 8. 파일 변경/커밋/푸시
        try:
            pr_procedure.change_files()
            self.result["change_files"] = True
        except Exception as e:
            self.result["error_msg"] = f"change_files: {e}"
            return self.result

        # 9. 메인 브랜치 찾기
        try:
            pr_procedure.current_main_branch()
            self.result["get_main_branch"] = True
        except Exception as e:
            self.result["error_msg"] = f"get_main_branch: {e}"
            return self.result

        # 10. PR 생성 (내 fork 기준)
        try:
            pr_procedure.generate_pr()
            self.result["generate_pr"] = True
        except Exception as e:
            self.result["error_msg"] = f"generate_pr: {e}"
            return self.result

        # 11. 원본 PR 생성
        try:
            pr_procedure.create_pr_to_upstream()
            self.result["create_upstream_pr"] = True
        except Exception as e:
            self.result["error_msg"] = f"create_upstream_pr: {e}"
            return self.result
        return self.result
