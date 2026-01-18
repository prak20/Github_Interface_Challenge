from conftest import logger

def parse_star_count(star_text: str) -> int:
    """Convert star text like '123k' or '12,345' to integer, hmmm."""
    s = star_text.strip()
    if s.endswith('k'):
        return int(float(s[:-1]) * 1000)
    return int(s.replace(',', ''))

def log_step(message: str):
    logger.info(message)