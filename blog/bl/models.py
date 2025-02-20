from django.db import models

# Create your models here.
from os import path
import hashlib

import pypandoc


class MarkdownFile(models.Model):
    noteName = models.CharField(max_length=255, null=True)
    filePath = models.CharField(max_length=255)
    htmlFile = models.CharField(max_length=255, null=True, blank=True)

    fileHash = models.CharField(max_length=64)

    @classmethod
    def create(self, noteName, filePath, htmlFile):
        if path.isdir(filePath):
            return

        with open(filePath, 'rb') as f:
            currFileHash = hashlib.file_digest(f, 'sha256').hexdigest()

        markdownNoChange = MarkdownFile.objects.filter(
            fileHash=currFileHash).exists()

        # checks if theirs been a change in the file
        if markdownNoChange:
            return

        # delete old file, querys make sure location is the same
        MarkdownFile.objects.filter(filePath=filePath).delete()

        markdown = self(noteName=noteName,
                        filePath=filePath,
                        htmlFile=self.createHtmlFile(filePath, htmlFile),
                        fileHash=currFileHash)
        markdown.save()
        return markdown

    def createHtmlFile(markdownPath, htmlFile):
        try:
            pypandoc.convert_file(
                markdownPath,
                "html",
                outputfile=htmlFile,
                extra_args=['--mathjax',
                            '--include-in-header=/home/demirel/myworld/blog/bl/templates/mathJaxHeader.html'])

            return htmlFile

        except:
            return ""
