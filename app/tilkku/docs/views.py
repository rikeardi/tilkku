from django.shortcuts import render, redirect
from .models import *


# Create your views here.
def home(request):
    context = {
        'headers': DocsHeader.objects.all(),
        'pages': DocsPage.objects.all(),
        'chapters': DocsChapter.objects.all(),
        'page': None,
    }
    return render(request, 'docs/front.html', context)


def header_delete(request, id):
    header = DocsHeader.objects.get(id=id)
    header.delete()
    return redirect('/docs/')


def header_edit(request, id):
    header = DocsHeader.objects.get(id=id)

    if request.method == 'POST':
        header.title = request.POST['title'].lower()
        header.save()
        return redirect('/docs/')

    return redirect('/docs/')


def header_new(request):
    if request.method == 'POST':
        header = DocsHeader.objects.create(title=request.POST['title'].lower())
        header.save()
        return redirect('/docs/')


def page(request, page_name):
    page = DocsPage.objects.get(title=page_name)
    context = {
        'headers': DocsHeader.objects.all(),
        'pages': DocsPage.objects.all(),
        'chapters': DocsChapter.objects.all(),
        'page': page,
        'page_chapters': DocsChapter.objects.filter(page_id=page.id),
    }
    return render(request, 'docs/front.html', context)


def page_delete(request, id):
    page = DocsPage.objects.get(id=id)
    page.delete()
    return redirect('/docs/')


def page_edit(request, id):
    page = DocsPage.objects.get(id=id)

    if request.method == 'POST':
        page.title = request.POST['title'].lower()
        page.save()
        return redirect('/docs/' + page.title + '/')

    return redirect('/docs/' + page.title + '/')


def page_new(request):
    if request.method == 'POST':
        page = DocsPage.objects.create(title=request.POST['title'].lower(),
                                       header_id=request.POST['header_id'])
        page.save()
        return redirect('/docs/' + page.title + '/')


def chapter_delete(request, id):
    chapter = DocsChapter.objects.get(id=id)
    chapter.delete()
    return redirect('/docs/' + chapter.page.title + '/')


def chapter_edit(request, id):
    chapter = DocsChapter.objects.get(id=id)

    if request.method == 'POST':
        chapter.title = request.POST['title'].lower()
        chapter.save()
        return redirect('/docs/' + chapter.page.title + '/')

    return redirect('/docs/' + chapter.page.title + '/')


def chapter_new(request):
    if request.method == 'POST':
        chapter = DocsChapter.objects.create(title=request.POST['title'].lower(),
                                             page_id=request.POST['page_id'])
        chapter.save()
        chapter.page = DocsPage.objects.get(id=request.POST['page_id'])
        return redirect('/docs/' + chapter.page.title + '/')


def section_delete(request, id):
    section = DocsSection.objects.get(id=id)
    section.delete()
    return redirect('/docs/')


def section_edit(request, id):
    section = DocsSection.objects.get(id=id)

    if request.method == 'POST':

        if request.POST.get('text'):
            section.text = request.POST['text']
        if request.POST.get('image'):
            print(request.POST['image'])
        section.save()
        return redirect('/docs/')

    return redirect('/docs/')


def section_new(request):
    if request.method == 'POST':
        section = DocsSection.objects.create(text=request.POST['text'].lower(),
                                             order=request.POST['order'],
                                             chapter_id=request.POST['chapter_id'])
        section.save()
        return redirect('/docs/')
