# -*- coding: utf-8 -*-
from pelican import signals, contents
from git import Git, Repo, InvalidGitRepositoryError
import os
from datetime import datetime
from time import mktime, altzone

import locale
locale.setlocale(locale.LC_ALL, 'C')

try:
    repo = Repo(os.path.abspath('.'))
    git = Git(os.path.abspath('.'))
except InvalidGitRepositoryError as e:
    repo = None

def specs(content):
    if isinstance(content, contents.Static) \
       or repo is None \
       or content.metadata.get('scep', None) is None:
        return

    scep = int(content.metadata.get('scep'))
    content.template = 'spec'
    content.slug = 'scep%04d' % scep

    path = content.source_path
    status, stdout, stderr = git.execute(['git', 'ls-files', path, '--error-unmatch'],
            with_extended_output=True, with_exceptions=False)
    if status != 0:
        # file is not managed by git
        content.updated = datetime.fromtimestamp(os.stat(path).st_mtime)
        content.gitrev = '(not yet committed)'
    else:
        commits = repo.commits(path=path)
        assert len(commits) > 0
        content.updated = datetime.fromtimestamp(mktime(commits[-1].committed_date) - altzone)
        content.gitrev = commits[-1].id

    content.updated = content.updated.strftime('%F %T %z (%a, %d %B %Y)')
    content.status = 'hidden'
    content.scep_status = content.metadata.get('status')

def register():
    signals.content_object_init.connect(specs)
