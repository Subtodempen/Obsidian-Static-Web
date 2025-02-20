from django.shortcuts import render
from django.http import HttpResponse
from .models import MarkdownFile

from django.db.models import Q
from django.db.models.query import QuerySet

from os import listdir
from os import path

import urllib.parse

obsidianVaultPath = r"/home/demirel/New Vault"


def openNote(request, blogTitle, noteName):
    note = MarkdownFile.objects.filter(
        Q(filePath__contains=blogTitle) & Q(filePath__contains=noteName)
    )

    if not note:
        return HttpResponse("Error file not found")

    elif isinstance(note, QuerySet):
        note = note.first()

    htmlFile = open(note.htmlFile)
    htmlData = htmlFile.read()
    htmlFile.close()

    return render(request, "genericNote.html", {"noteHtml": htmlData, "name": noteName})


def openFolder(request, blogTitle, filePath):
    dirNames = listdir(filePath)

    blogFiles = []
    blogFolders = []

    for file in dirNames:
        file = urllib.parse.quote(file)

        if path.isdir(file):
            blogFolders.append(file)
            continue

        blogFiles.append(file)

    #    if blogTitle in dirNames:
    #   blogFiles = MarkdownFile.objects.filter(filePath__contains=blogTitle)

    currUrl = urllib.parse.quote(request.path)

    return render(request, 'genericTopicPage.html',
                  {'blogFolders': blogFolders,
                   'blogFiles': blogFiles,
                   'Title': blogTitle,
                   'currUrl': currUrl})


# Checks if it is a File or a folder,
# if folder than use the folder view and so on.
def dynamicFileRouter(request, blogTitle):
    filePath = obsidianVaultPath + '/' + blogTitle

    if path.isfile(filePath):
        blogName = blogTitle.split('/')[-1]
        return openNote(request, blogTitle, blogName)

    return openFolder(request, blogTitle, filePath)


def members(request):
    # iterate over file paths and display them as a link.
    # get all files from /home/demirel/new Vaulr

    dirNamesAndPaths = getDirNameAndPath(obsidianVaultPath)

    # Append refresh object to menu
    dirNamesAndPaths = list(dirNamesAndPaths)
    dirNamesAndPaths.append(('Refresh', '/refresh'))
    zip(dirNamesAndPaths)

    return render(
        request, 'index.html', {'dirNamesAndPaths': dirNamesAndPaths})


def getDirNameAndPath(vaultPath):
    dirNames = listdir(vaultPath)

    urlPaths = []  # both contain path to markdown

    for dirName in dirNames:
        path = 'vault/' + dirName
        linkUrl = urllib.parse.quote(path)

        urlPaths.append(linkUrl)

    return zip(dirNames, urlPaths)


def createMarkdownModel(vaultPath):
    dirNames = listdir(vaultPath)
    htmlPathName = "/home/demirel/myworld/blog/bl/templates/htmlDocs/"

    for fName in dirNames:
        markdownFile = vaultPath + "/" + fName

        if (path.isdir(markdownFile)):
            createMarkdownModel(markdownFile)
            continue

        MarkdownFile.create(
            fName, markdownFile, htmlPathName + fName + '.html')


def refreshModel(request):
    createMarkdownModel(obsidianVaultPath)

    return HttpResponse("Refreshed")
