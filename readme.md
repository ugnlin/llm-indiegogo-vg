# Kickstarter Game LLM Scraper Predictor

quick little project to try the following things:
- Scrape games off of kickstarter
- Use LLaMa to engineer a bunch of features (fine tuning/direct prediction will take too long but could also be fun 
another time)
- Do the standard data science prediction pipeline to predict % of original goal funded

I chose this project to show off my scrappy agile python skills. I have actual professional experience in my field, so
I'm just looking to do a technical project here. The domain is for fun, to keep me motivated to build this out as I'm
expecting it just to be for personal gain!

Requirements:
- `pip install -r requirements.txt`
- a llama-cpp-python installation: here's a precompiled whl that uses cuBLAS (for gpu)
- `python -m pip install llama-cpp-python --prefer-binary --extra-index-url=https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/AVX2/cu118`
- a gguf file (the llm) pointed at in the .env
- a tokenizer (eg. llama 2 tokenizer) pointed at in the .env

To-improve list
- Scrape number of pictures in description since some projects like making tons of graphics and putting info in those 
and not writing a description
- Scrape pledge tiers