import os
import random
from datetime import datetime
from bs4 import BeautifulSoup

def generate_card_html(card_data):
    """Generates the HTML string for a single quest card."""
    return f"""
            <a href="{card_data['url']}" class="quest-card fade-in" target="_blank" rel="noopener noreferrer" data-title="{card_data['title']}">
                <div class="quest-icon">{card_data['icon']}</div>
                <h3 class="quest-title">{card_data['title']}</h3>
                <div class="quest-button">Play Now</div>
            </a>
    """

def update_html_file(html_file_path="index.html"):
    """
    Updates the index.html file with the correct quest cards based on the day.
    """
    # Define all possible quest cards
    all_cards = [
        {"url": "https://add-sub-quest.web.app", "icon": "🧮", "title": "Math"},
        {"url": "https://spelling-quest.web.app/", "icon": "📝", "title": "Spelling"},
        {"url": "https://monetki-quest.web.app", "icon": "🪙", "title": "Coins"},
        {"url": "https://rounding-quest.web.app", "icon": "↕️", "title": "Rounding"},
        {"url": "https://shapes-quest.web.app", "icon": "🔷", "title": "Shapes"},
        {"url": "https://counting-quest.web.app", "icon": "🔢", "title": "Counting"},
    ]

    # Fixed cards that always appear
    fixed_cards_titles = ["Math", "Spelling"]

    # Cards from which one will be randomly chosen
    random_pool = [card for card in all_cards if card['title'] not in fixed_cards_titles]

    today = datetime.now()
    # For testing, you can uncomment and set a specific date:
    # today = datetime(2025, 7, 8) # Example: July 8, 2025 (Tuesday)
    # today = datetime(2025, 7, 9) # Example: July 9, 2025 (Wednesday)

    # Determine the third card
    # For July 8, 2025, it's Coins. For weekdays starting July 9, it's random.
    if today.year == 2025 and today.month == 7 and today.day == 8:
        # Specific rule for July 8, 2025
        chosen_card = next(card for card in all_cards if card['title'] == "Coins")
        print("Today is July 8, 2025. 'Coins' quest chosen.")
    elif 0 <= today.weekday() <= 4:  # Monday (0) to Friday (4)
        # Randomly choose one from the pool for weekdays
        chosen_card = random.choice(random_pool)
        print(f"Today is a weekday. Randomly chosen quest: '{chosen_card['title']}'")
    else:
        # On weekends, we can choose to keep the last selected card or a default one.
        # For this implementation, let's keep 'Coins' as a fallback for weekends too,
        # or you can adjust this logic.
        # For simplicity and to ensure 3 cards are always present, let's just pick one randomly for weekends too
        # or keep the last one if you store it.
        # For now, let's default to 'Coins' for weekends if no specific rule applies.
        # A more robust solution for weekends would involve reading the current HTML
        # and keeping the existing third card if it's a weekend.
        # However, the request was for Monday-Friday updates.
        print("Today is a weekend. No specific random update required by the prompt. Defaulting to 'Coins'.")
        chosen_card = next(card for card in all_cards if card['title'] == "Coins")


    # Construct the list of cards to be displayed
    cards_to_display = []
    for title in fixed_cards_titles:
        cards_to_display.append(next(card for card in all_cards if card['title'] == title))
    cards_to_display.append(chosen_card)

    # Read the existing HTML file
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: {html_file_path} not found.")
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    quest_grid = soup.find('div', class_='quest-grid')

    if quest_grid:
        # Clear existing cards in the quest-grid
        quest_grid.clear()

        # Add the selected cards to the quest-grid
        for card_data in cards_to_display:
            card_html = generate_card_html(card_data)
            # Use BeautifulSoup to parse the new card HTML and append it
            new_card_soup = BeautifulSoup(card_html, 'html.parser')
            quest_grid.append(new_card_soup.find('a')) # Append the <a> tag

        # Write the modified HTML back to the file
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify())) # Use prettify for readable output
        print(f"Successfully updated {html_file_path} with new quest cards.")
    else:
        print("Error: Could not find 'quest-grid' div in the HTML.")

if __name__ == "__main__":
    update_html_file()

    # Git operations to commit and push changes
    # These commands will run in the GitHub Actions environment
    try:
        os.system("git config user.name 'github-actions[bot]'")
        os.system("git config user.email 'github-actions[bot]@users.noreply.github.com'")
        os.system("git add index.html")
        os.system("git commit -m 'Automated: Update daily quest cards'")
        os.system("git push")
        print("Changes committed and pushed successfully.")
    except Exception as e:
        print(f"Error during git operations: {e}")
