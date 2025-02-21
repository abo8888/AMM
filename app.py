from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

DATABASE_URL = "postgresql://db_amm_user:Jose0OSs5MyWmFTbrWdDhO1xCUKvGauj@dpg-curr0s23esus73ffq1ng-a.oregon-postgres.render.com:5432/db_amm"

def get_articles():
    """ Fetch all articles from the database """
    articles = []
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, content, image FROM articles ORDER BY id DESC")
        rows = cursor.fetchall()
        for row in rows:
            articles.append({
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "image_url": row[3] if row[3] else "https://via.placeholder.com/600x400"
            })
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error fetching articles: {e}")
    return articles

@app.route('/')
def index():
    articles = get_articles()
    return render_template('index.html', articles=articles)

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    """ Fetch a specific article by ID """
    article = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT title, content, image FROM articles WHERE id = %s", (article_id,))
        row = cursor.fetchone()
        if row:
            article = {
                "title": row[0],
                "content": row[1],
                "image_url": row[2] if row[2] else "https://via.placeholder.com/600x400"
            }
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error fetching article: {e}")
    
    if article:
        return render_template('article.html', article=article)
    else:
        return "<h1>Article not found</h1>", 404

if __name__ == '__main__':
    app.run(debug=True)
