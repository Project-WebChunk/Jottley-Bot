from pymongo import MongoClient
from uuid import uuid4
import random
import datetime
import requests


class Database:
    def __init__(self, URL):
        self.client = MongoClient(URL)
        self.db = self.client.Jottley
        self.users = self.db.users
        self.books = self.db.books

    def userExists(self, id):
        return self.users.find_one({'discord': id}) is not None

    def getUser(self, id):
        return self.users.find_one({'discord': id})

    def updateName(self, email, name):
        self.users.update_one({'email': email}, {'$set': {'username': name}})
        return True

    def generateID(self):
        return "".join(random.choice("0123456789ABCDEF") for i in range(10))

    def createBook(self, id, name):
        bookID = self.generateID()
        book = {
            "_id": bookID,
            "name": name,
            "chapters": {},
            "chapterOrder": [],
            "by": id
        }
        self.books.insert_one(book)
        self.users.update_one({'_id': id}, {'$push': {'books': bookID}})
        bookIndex = self.users.find_one({'_id': id})['books'].index(bookID)
        return bookID, bookIndex

    def createChapter(self, bookID, name):
        chapterID = self.generateID()
        chapter = {
            "_id": chapterID,
            "name": name,
            "snippets": {},
            "snippetOrder": []
        }

        self.books.update_one(
            {'_id': bookID}, {'$set': {'chapters.' + chapterID: chapter}})
        self.books.update_one(
            {'_id': bookID}, {'$push': {'chapterOrder': chapterID}})
        
        chapterIndex = self.books.find_one({'_id': bookID})['chapterOrder'].index(chapterID)
        bookIndex = self.users.find_one({'_id': bookID})['books'].index(bookID)
        return {"chapterIndex": chapterIndex, "bookIndex": bookIndex, 
                "ids": [bookID, chapterID]}

    def createSnippet(self, bookID, chapterID, name):
        snippetID = self.generateID()
        snippet = {
            "_id": snippetID,
            "name": name,
            "content": ""
        }
        self.books.update_one(
            {'_id': bookID}, {'$set': {'chapters.' + chapterID + '.snippets.' + snippetID: snippet}})
        self.books.update_one(
            {'_id': bookID}, {'$push': {'chapters.' + chapterID + '.snippetOrder': snippetID}})
        
        book = self.books.find_one({'_id': bookID})
        
        snippetIndex = book['chapters'][chapterID]['snippetOrder'].index(snippetID)
        chapterIndex = book['chapterOrder'].index(chapterID)
        bookIndex = self.users.find_one({'_id': bookID})['books'].index(bookID)
        
        return {"snipIndex": snippetIndex, "chapterIndex": chapterIndex, 
                "bookIndex": bookIndex, "ids": [bookID, chapterID, snippetID]}

    def getBook(self, bookID):
        return self.books.find_one({'_id': bookID})

    def getSnippet(self, bookID, chapterID, snippetID):
        book = self.books.find_one({'_id': bookID})
        return book['chapters'][chapterID]['snippets'][snippetID]

    def deleteBook(self, bookID):
        book = self.books.find_one({'_id': bookID})
        self.books.delete_one({'_id': bookID})
        self.users.update_one({'_id': book['by']}, {
                              '$pull': {'books': bookID}})

    def deleteChapter(self, bookID, chapterID):
        self.books.update_one(
            {'_id': bookID}, {'$unset': {'chapters.' + chapterID: 1}})
        self.books.update_one(
            {'_id': bookID}, {'$pull': {'chapterOrder': chapterID}})

    def deleteSnippet(self, bookID, chapterID, snippetID):
        self.books.update_one({'_id': bookID}, {'$unset': {
                              'chapters.' + chapterID + '.snippets.' + snippetID: 1}})
        self.books.update_one({'_id': bookID}, {
                              '$pull': {'chapters.' + chapterID + '.snippetOrder': snippetID}})

    def updateSnippetContent(self, bookID, chapterID, snippetID, content):
        self.books.update_one({'_id': bookID}, {'$set': {
                              'chapters.' + chapterID + '.snippets.' + snippetID + '.content': content}})

    def updateSnippet(self, bookID, chapterID, snippetID, name):
        self.books.update_one({'_id': bookID}, {
                              '$set': {'chapters.' + chapterID + '.snippets.' + snippetID + '.name': name}})

    def updateChapter(self, bookID, chapterID, name):
        self.books.update_one(
            {'_id': bookID}, {'$set': {'chapters.' + chapterID + '.name': name}})

    def updateBook(self, bookID, name):
        self.books.update_one({'_id': bookID}, {'$set': {'name': name}})
