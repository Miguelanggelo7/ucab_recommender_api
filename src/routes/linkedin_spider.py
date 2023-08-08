import subprocess

def run_linkedin_spider():
    resultado = subprocess.run(
        "scrapy runspider src/spiders/linkedinspider.py", shell=True)

    print(resultado)
    if resultado.returncode == 0:
        return "dsdxad"
    else:
        return f"Error: {resultado}"