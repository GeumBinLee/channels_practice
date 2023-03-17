from django.shortcuts import get_list_or_404
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from places.models import Place
from reviews.models import Comment, Recomment, Review
from reviews.serializers import (CommentCreateSerializer, CommentSerializer,
                                 RecommentCreateSerializer,
                                 RecommentSerializer, ReviewCreateSerializer,
                                 ReviewDetailSerializer, ReviewListSerializer)


#####리뷰#####
class ReviewListView(APIView):
    permissions_classes = [AllowAny] 

    #장소 리뷰 리스트
    def get(self, request, place_id):
        review = get_list_or_404(Review, place_id=place_id)
        serializer = ReviewListSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #리뷰 작성
    def post(self, request, place_id):
        if request.user:
            serializer = ReviewCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, place_id=place_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

class ReviewDetailView(APIView):
    permissions_classes = [IsAuthenticated]

    #리뷰 상세 페이지
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        serializer = ReviewDetailSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #리뷰 수정
    def put(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.author:
            serializer = ReviewCreateSerializer(review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(author=request.user, review_id=review_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

# 리뷰 좋아요
class ReviewLikeView(APIView):
    permissions_classes = [IsAuthenticated] 

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if request.user in review.review_like.all():
            review.review_like.remove(request.user)
            return Response({"message":"리뷰 좋아요를 취소했습니다"}, status=status.HTTP_200_OK)
        else:
            review.review_like.add(request.user)
            return Response({"message":"리뷰 좋아요를 했습니다."}, status=status.HTTP_200_OK)

#####댓글#####
class CommentListView(APIView):
    permissions_classes = [IsAuthenticated] 

    # 댓글 조회
    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        comments = review.review_comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 댓글 작성
    def post(self, request, review_id):
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, review_id=review_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    permissions_classes = [IsAuthenticated] 

    # 댓글 수정
    def put(self, request, review_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.author:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, review_id=review_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

    # 댓글 삭제
    def delete(self, request, review_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.author:
            comment.delete()
            return Response({"message":"댓글 삭제 완료"},status=status.HTTP_200_OK)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

# 댓글 좋아요
class CommentLikeView(APIView):
    permissions_classes = [IsAuthenticated] 

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.comment_like.all():
            comment.comment_like.remove(request.user)
            return Response({"message":"댓글 좋아요를 취소했습니다"}, status=status.HTTP_200_OK)
        else:
            comment.comment_like.add(request.user)
            return Response({"message":"댓글 좋아요를 했습니다"}, status=status.HTTP_200_OK)

#####대댓글##### 
class RecommentListView(APIView):
    permissions_classes = [IsAuthenticated] 

    # 대댓글 조회
    def get(self, request, review_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        recomments = comment.comment_recomments.all()
        serializer = RecommentSerializer(recomments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 대댓글 작성
    def post(self, request, review_id, comment_id):
        serializer = RecommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, comment_id=comment_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecommentDetailView(APIView):
    permissions_classes = [IsAuthenticated] 

    # 대댓글 수정
    def put(self, request, review_id, comment_id, recomment_id):
        recomment = get_object_or_404(Recomment, id=recomment_id)
        if request.user == recomment.author:
            serializer = RecommentCreateSerializer(recomment, data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, comment_id=comment_id)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

    # 대댓글 삭제
    def delete(self, request, review_id, comment_id, recomment_id):
        recomment = get_object_or_404(Recomment, id=recomment_id)
        if request.user == recomment.author:
            recomment.delete()
            return Response({"message":"대댓글 삭제 완료"},status=status.HTTP_200_OK)
        return Response({"message":"접근 권한 없음"}, status=status.HTTP_403_FORBIDDEN)

# 대댓글 좋아요
class RecommentLikeView(APIView):
    permissions_classes = [IsAuthenticated] 

    def post(self, request, recomment_id):
        recomment = get_object_or_404(Recomment, id=recomment_id)
        if request.user in recomment.recomment_like.all():
            recomment.recomment_like.remove(request.user)
            return Response("대댓글 좋아요취소했습니다.", status=status.HTTP_200_OK)
        else:
            recomment.recomment_like.add(request.user)
            return Response("대댓글 좋아요했습니다.", status=status.HTTP_200_OK)