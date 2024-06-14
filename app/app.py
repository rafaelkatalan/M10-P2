from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import logging

app = FastAPI()
blog_posts = []

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='blog.log')
logger = logging.getLogger(__name__)

class BlogPost:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content

    def __str__(self) -> str:
        return f'{self.id} - {self.title} - {self.content}'
    
    def toJson(self):
        return {'id': self.id, 'title': self.title, 'content': self.content}

class Blog(BaseModel):
    id: int
    title: str
    content: str

@app.post('/blog')
def create_blog_post(data: Blog):
    try:
        blog_posts.append(BlogPost(data.id, data.title, data.content))
        logger.info(f"Created blog post with ID: {data.id}")
        return {'status': 'success'}
    except KeyError:
        logger.error('Invalid request')
        raise HTTPException(status_code=400, detail='Invalid request')
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/blog')
def get_blog_posts():
    try:
        logger.info("Retrieving all blog posts")
        return ({'posts': [blog.toJson() for blog in blog_posts]}), 200
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/blog/{id}')
def get_blog_post(id:int):
    for post in blog_posts:
        if post.id == id:
            logger.info(f"Retrieving blog post with ID: {id}")
            return ({'post': post.__dict__})
    logger.error(f"Post with ID: {id} not found")
    raise HTTPException(status_code=404, detail='Post not found')


@app.delete('/blog/{id}')
def delete_blog_post(id:int):
    for post in blog_posts:
        if post.id == id:
            blog_posts.remove(post)
            logger.info(f"Deleted blog post with ID: {id}")
            return {'status':'success'}
    logger.error(f"Post with ID: {id} not found")
    raise HTTPException(status_code=404, detail='Post not found')


@app.put('/blog/{id}')
def update_blog_post(id:int, data: Blog):
    try:
        for post in blog_posts:
            if post.id == id:
                post.title = data.title
                post.content = data.content
                logger.info(f"Updated blog post with ID: {id}")
                return {'status':'success'}
        logger.error(f"Post with ID: {id} not found")
        raise HTTPException(status_code=404, detail='Post not found')
    except KeyError:
        logger.error('Invalid request')
        raise HTTPException(status_code=400, detail='Invalid request')
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__': 
    uvicorn.run(app, host="0.0.0.0", port=8001)
