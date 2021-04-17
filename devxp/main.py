
import xpanalyser


if __name__ == "__main__":
    GIT_PATH = "..\\test\\warp"
    WORK_DIR = "..\\output\\"
    xp_analyser = xpanalyser.XPAnalyser(GIT_PATH, WORK_DIR)
    xp_analyser.compute_experience()
