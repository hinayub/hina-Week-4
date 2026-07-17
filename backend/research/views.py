from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .agent import run_research
from .models import ResearchQuery
from .serializers import ResearchQuerySerializer

# How many recent Q&A turns to feed back to the agent as session memory.
MEMORY_TURNS = 6


class ResearchView(APIView):
    """POST a question; the agent researches it with web search and answers."""

    def post(self, request):
        query = (request.data.get("query") or "").strip()
        if not query:
            return Response(
                {"error": "A non-empty 'query' field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Build the memory: the user's earlier messages, oldest first, so the
        # agent can recall facts from earlier in the session.
        recent = ResearchQuery.objects.all()[:MEMORY_TURNS]
        memory = [r.query for r in reversed(list(recent))]

        try:
            result = run_research(query, memory=memory)
        except Exception as exc:  # surface agent/LLM failures cleanly
            return Response(
                {"error": f"Research failed: {exc}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        record = ResearchQuery.objects.create(
            query=query,
            answer=result["answer"],
            sources=result["sources"],
        )
        return Response(
            ResearchQuerySerializer(record).data,
            status=status.HTTP_201_CREATED,
        )


class ResearchHistoryView(ListAPIView):
    """List past research queries, newest first."""

    queryset = ResearchQuery.objects.all()
    serializer_class = ResearchQuerySerializer
