# Your name: Matt Kish
# Your student id:
# Your email:
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def check_tables_in_db(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())
    conn.close()

check_tables_in_db('South_U_Restaurants.db')


def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT * FROM restaurants")
    rows = cur.fetchall()

    rest_data = {}
    for row in rows:
        rest_data[row[0]] = {'category': row[1], 'building': row[2], 'rating': row[3]}
    conn.close()
    return rest_data
    pass

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT category., COUNT(*) FROM restaurants GROUP BY category")
    rows = cur.fetchall()
    
    cat_data = {row[0]: row[1] for row in rows}
    plt.bar(cat_data.keys(), cat_data.values())
    plt.xticks(rotation=90)
    plt.ylabel('Number of Restaurants')
    plt.title('Restaurant Categories')
    plt.show()
    conn.close()
    return cat_data
    pass

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT name FROM restaurants WHERE building=? ORDER BY rating DESC", (building_num,))
    rows = cur.fetchall()

    rest_list = [row[0] for row in rows]
    conn.close()
    return rest_list
    pass

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT category, AVG(rating) AS avg_rating FROM restaurants GROUP BY category ORDER BY avg_rating DESC")
    cat_rows = cur.fetchall()
    cur.execute("SELECT building, AVG(rating) AS avg_rating FROM restaurants GROUP BY building ORDER BY avg_rating DESC")
    build_rows = cur.fetchall()

    highest_rating = [cat_rows[0], build_rows[0]]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.barh([row[0] for row in cat_rows], [row[1] for row in cat_rows])
    ax1.set_xlabel('Average Rating')
    ax1.set_title('Categories')
    ax2.barh([row[0] for row in build_rows], [row[1] for row in build_rows])
    ax2.set_xlabel('Average Rating')
    ax2.set_title('Buildings')
    plt.show()
    conn.close()
    return highest_rating
    pass

#Try calling your functions here
def main():
    print(load_rest_data('South_U_Restaurants.db'))
    print(plot_rest_categories('South_U_Restaurants.db'))
    print(find_rest_in_building(1140, 'South_U_Restaurants.db'))
    print(get_highest_rating('South_U_Restaurants.db'))
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
