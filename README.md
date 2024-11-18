# What’s On  
## Your Personalized AI News Companion  

---

## Abstract  
In the digital age, users face the challenge of navigating excessive and often irrelevant content. What’s On is an AI-powered conversational assistant designed to address this issue by providing real-time news updates, concise summaries, and hands-free text-to-speech functionality. Deployed on Render and powered by IBM watsonx Assistant, the application simplifies news consumption through natural, dynamic interactions.

---

## 1. Basic Information

### Short Description  
What’s On is an AI-powered assistant that delivers real-time news, generates summaries, and enables text-to-speech functionality.  

---

### Long Description  

#### The Problem  
The abundance of irrelevant or lengthy digital content overwhelms users, making it challenging to stay informed. This leads to wasted time and missed opportunities for critical insights.  

#### The Solution  
What’s On addresses this by aggregating news from trusted sources, generating concise summaries, and providing dynamic interactions. Powered by IBM watsonx Assistant, the app ensures efficient and accessible news consumption, conversational assistance with general reponses.  

#### Key Features  
- News Aggregation: Fetches news updates instantly from trusted sources based on queries.  
- AI-Powered Summarization: Condenses lengthy articles into digestible insights.  
- Text-to-Speech: Reads summaries aloud for hands-free convenience.  
- Dynamic Conversations: Engages users naturally via AI-driven interactions.  

#### Target Audience  
Busy professionals, students, and individuals seeking concise, accessible news updates while maintaining good conversation .

---

## 2. System Overview  

### Features  
1. News Updates: Instant access to current events tailored to user queries.  
2. Concise Summaries: News articles are reduced to key points for efficient consumption.  
3. Text-to-Speech: Hands-free consumption of news summaries.  
4. Conversational AI: Engages users with natural, context-aware interactions.  

---

### Workflow  
1. *User Query: The user submits a question, e.g., *“What’s the latest in technology?”  
2. Processing:  
   - The Flask backend routes the query to IBM watsonx Assistant for natural language processing.  
   - NewsAPI provides real-time news data, which is summarized using NLP tools.  
3. Response Delivery: The system returns a concise summary in text and/or audio format.  

---

### Technical Architecture  
plaintext
User → Flask Backend → IBM watsonx Assistant → NewsAPI → User

 


| Component            | Description                                              |  
|---------------------------|--------------------------------------------------------------|  
| Frontend              | A simple text-based input and output interface.              |  
| Backend               | Flask application managing API requests and response logic. |  
| IBM watsonx Assistant | Processes user queries and generates responses.              |  
| NewsAPI               | Provides real-time news articles from trusted sources.       |  
| Text-to-Speech        | Converts textual summaries into audio outputs.               |  

---

## 3. Deployment  

### Hosting on Render  
The application is hosted on Render for scalability and reliability.  

- Build Command:  
  bash
  pip install -r requirements.txt
    

- Start Command:  
  bash
  gunicorn app:app
    

- Environment Variables:  
  - WATSON_API_KEY: API key for IBM watsonx Assistant.  
  - WATSON_URL: Endpoint for IBM watsonx Assistant.  
  - NEWS_API_KEY: API key for NewsAPI.  

Live Application URL: [Insert Render URL here]  

---

## 4. Results and Demonstration  

### Interaction Example  
1. *User Query: *“What’s the latest in technology?”  
2. Response: A concise summary of the latest technology news.  
3. Text-to-Speech: The summary is optionally read aloud for hands-free use.  

---

## 5. Challenges and Solutions  

### Challenges  
- API Rate Limits: Efficient batching of requests was implemented to avoid exceeding API quotas.  
- Integration Complexity: Coordination between multiple APIs required troubleshooting for smooth responses.  

### Solutions  
- Optimized API calls to ensure minimal latency.  
- Streamlined Flask backend to handle concurrent user queries.  

---

## 6. Future Enhancements  

### Scalability Goals  
1. leverage IBM solutions: IBM provides enough tools from training to fine-tuning models that could enhance the app
2. Multi-Language Support: Use IBM Language Translator to support non-English users.  
3. Voice Interaction: Enable hands-free interaction with IBM Watson Speech-to-Text.  
4. User Personalization: Add accounts for personalized news feeds.  
5. Analytics Dashboard: Provide insights into user behavior and popular queries. 
6. GUI enhancements: For a more user-friendly experience


---

## 7. Conclusion  
What’s On provides an accessible, AI-driven solution to information consumption and overload. By combining real-time news aggregation, summarization, and conversational interactions, it simplifies how users stay informed. Future enhancements will focus on personalization, scalability, and expanded accessibility, ensuring the app evolves to meet diverse user needs.

---

## 8. References  
- IBM watsonx Assistant Documentation  
- NewsAPI Developer Guide  
- Flask Documentation
