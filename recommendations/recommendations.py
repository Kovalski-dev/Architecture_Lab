# recommendations/recommendations.py

from concurrent import futures
import random

import grpc 

from recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse,
)
import recommendations_pb2_grpc

books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="Unlocking Android"),
        BookRecommendation(id=2, title="Android in Action, Second Edition"),
        BookRecommendation(id=3, title="Specification by Example"),
        BookRecommendation(id=4, title="Flex 3 in Action"),
        BookRecommendation(id=5, title="Flex 4 in Action"),
        BookRecommendation(id=6, title="Collective Intelligence in Action"),
        BookRecommendation(id=7, title="Zend Framework in Action"),
        BookRecommendation(id=8, title="Flex on Java"),
        BookRecommendation(id=9, title="Griffon in Action"),
        BookRecommendation(id=10, title="OSGi in Depth"),
    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(id=1, title="Flexible Rails"),
        BookRecommendation(id=2, title="Hello! Flex 4"),
        BookRecommendation(id=3, title="Coffeehouse"),
        BookRecommendation(id=4, title="Team Foundation Server 2008 in Action"),
        BookRecommendation(id=5, title="Brownfield Application Development in .NET"),
        BookRecommendation(id=6, title="MongoDB in Action"),
        BookRecommendation(id=7, title="Distributed Application Development with PowerBuilder 6.0"),
        BookRecommendation(id=8, title="Jaguar Development with PowerBuilder 7"),
        BookRecommendation(id=9, title="Taming Jaguar"),
        BookRecommendation(id=10, title="3D User Interfaces with Java 3D"),
    ],
    BookCategory.SELF_HELP: [
        BookRecommendation(id=1, title="Hibernate in Action"),
        BookRecommendation(id=2, title="JSTL in Action"),
        BookRecommendation(id=3, title="iBATIS in Action"),
        BookRecommendation(id=4, title="Designing Hard Software"),
        BookRecommendation(id=5, title="Hibernate Search in Action"),
        BookRecommendation(id=6, title="Ruby for Rails"),
        BookRecommendation(id=7, title="The Well-Grounded Rubyist"),
        BookRecommendation(id=8, title="Website Owner's Manual"),
        BookRecommendation(id=9, title="Hello! Python"),
        BookRecommendation(id=10, title="PFC Programmer's Reference Manual"),
    ],
}

class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")
        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(books_for_category, num_results)
        return RecommendationResponse(recommendations=books_to_recommend)
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
    RecommendationService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
if __name__ == "__main__":
    serve()