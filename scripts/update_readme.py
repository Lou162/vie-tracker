from scraper import scrape_offers
from datetime import datetime

def update_readme():
    print("Updating README.md with the latest offers...")
    result = scrape_offers()
    if result is None:
        print("No offers found.")
        return
    readme_file = open("./README.md","r+",encoding = "utf-8")
    readme_lines = readme_file.readlines()
    dateLine = readme_lines.index("<!-- Date de mise à jour -->\n")
    readme_lines[dateLine+2] = f"**Dernière mise à jour:** {datetime.now().strftime('%d/%m/%Y')}\n"
    for country, offers in result.items():
        print(f"Updating offers for {country}...")
        title_line = readme_lines.index(f"<!-- Title {country} -->\n")
        readme_lines[title_line+2] = f"## {country} <span style='color:gray'>({len(offers)} offres)</span>\n"
        line = readme_lines.index(f"<!-- Ici les offres pour le {country} -->\n")
        end_line = readme_lines.index(f"<!-- Fin des offres pour le {country} -->\n")
        offers_details=[]
        for offer in offers:
            offers_details.append(f"{offer['company']} | {offer['mission']} | {offer['duration']} | {offer['contact']} | {offer['link']}\n")
            print(f"Adding offer: {offer['company']} | {offer['mission']} | {offer['duration']} | {offer['contact']} | {offer['link']}")
        readme_lines[line+4:end_line] = offers_details
    readme_file.close()
    readme_file = open("./README.md","w+",encoding = "utf-8")
    readme_file.writelines(readme_lines)

    #close both the files.
    readme_file.close()
    print("README.md updated successfully.")
update_readme()

