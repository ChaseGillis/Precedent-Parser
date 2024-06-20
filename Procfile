heroku config:set SCRAPEOPS_API_KEY=${{ secrets.SCRAPEOPS_API_KEY }} --app precedent-parser
heroku config:set OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }} --app precedent-parser
web: streamlit run Precedent_Parser.py --server.port $PORT