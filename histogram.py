import sqlite3
import matplotlib.pyplot as plt

# Function to fetch data from SQLite database
def fetch_data_from_db():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('data.db')

        # Example query to fetch age and name data (replace with your actual query)
        cursor = conn.cursor()
        query = "SELECT age, name FROM users WHERE age IS NOT NULL AND name IS NOT NULL"
        cursor.execute(query)

        # Fetch all rows from the result
        data = cursor.fetchall()

        # Close cursor and database connection
        cursor.close()
        conn.close()

        return data

    except sqlite3.Error as error:
        print(f"Error fetching data from SQLite: {error}")
        return None

# Function to create bar chart
def create_bar_chart(data):
    try:
        if not data:
            print("No data retrieved from the database.")
            return

        # Prepare data for plotting
        names = [row[1] for row in data]
        ages = [row[0] for row in data]

        # Plotting bar chart
        fig, ax = plt.subplots(figsize=(8, 6))  # Adjust figure size as needed
        bars = ax.barh(names, ages, color='skyblue')

        # Adding labels to bars
        for bar, name, age in zip(bars, names, ages):
            ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{name} ({age})',
                    ha='left', va='center', fontsize=10)

        # Describe x-axis and y-axis inside the figure
        plt.text(0.95, 0.95, 'X-axis: Name\nY-axis: Age', transform=ax.transAxes,
                 fontsize=10, ha='right', va='top', bbox=dict(facecolor='lightgray', alpha=0.5))

        plt.xlabel('Name')
        plt.ylabel('Age')
        plt.title('Bar Chart of Age by Name')
        plt.tight_layout()

        # Display the plot
        plt.show()

    except Exception as e:
        print(f"Error creating bar chart: {e}")

# Main function to run the script
if __name__ == "__main__":
    # Fetch data from database
    data = fetch_data_from_db()

    if data:
        # Create bar chart
        create_bar_chart(data)
