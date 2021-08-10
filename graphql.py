
# This is a simple tutorial to show how graphQL API can be implemented in python
"""
Step 1: Create Schema
GraphQL schema for extracting results from a website.
"""
import graphene
import extraction
import requests

def extract(url):
    html = requests.get(url).text
    extracted = extraction.Extractor().extract(html, source_url=url) # Gets HTLML page attributes
    # print(extracted)
    return extracted

class Website(graphene.ObjectType):
    url = graphene.String(required=True)
    title = graphene.String()
    description = graphene.String()
    image = graphene.String()
    feed = graphene.String()

    
class Query(graphene.ObjectType):
    website = graphene.Field(Website, url=graphene.String())

    def resolve_website(parent, info, url): # resolver for 'website' field in schema
        extracted = extract(url)
        return Website(url=url,
                       title=extracted.title,
                       description=extracted.description,
                       image=extracted.image,
                       feed=extracted.feed
        )
      
schema = graphene.Schema(query=Query)


"""
Step 2: Run GraphQL on Flask
Python HTTP server for GraphQL.
"""
from flask import Flask
from flask_graphql import GraphQLView


app = Flask(__name__)
app.add_url_rule('/', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
app.run()


"""
Step 3: Call the API with a query
Python HTTP server for GraphQL.
"""
import pprint

def query_url(url):
    q = """
    {
      website (url: "https://gmail.com" ) {    
        url
        title
        image
      }
    }
    """
    result = schema.schema.execute(q) # This function calls the qraphQL server and fetches the results
    if result.errors:
        if len(result.errors) == 1:
            raise Exception(result.errors[0])
        else:
            raise Exception(result.errors)
    return result.data


if __name__ == "__main__":
    results = query_url("https://gmail.com")
    pprint.pprint(results)


# Instructions to run
"""
mkdir gql
cd gql
python3 -m venv env
. ./env/bin/activate
pip install extraction graphene flask-graphql requests

python graphql.py
"""
