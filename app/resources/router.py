## router here will help us to figure out wether the question is faq  question or product inquiry

## when we will implement our UI ,we will be able to call this router code to route our question to faq or to diffrent pricing and inquiry

from semantic_router import Route
from semantic_router.layer import RouteLayer
from semantic_router.encoders import HuggingFaceEncoder


encoder=HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)
faq= Route(
    name='faq',
    utterances=[
        "What is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
    ]
)
sql=Route(
    name='sql',
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
    ]
)


router=RouteLayer(encoder=encoder,routes=[faq,sql]) ## in router layer we are supplying the routes and also the encoder

if __name__=="__main__":
    print(router("What is your policy on defective product?").name)
    print(router("Pink Puma shoes in price range 5000 to 1000").name)