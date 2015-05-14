# -*- coding: utf-8 -*-
from pelican import signals, contents
from git import Git, Repo, InvalidGitRepositoryError
import os
from datetime import datetime
import time
from sc import fp, fs

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

    # compute fingerprint
    fw = fs.fs_wrap(content.source_path)
    cv = fp.compute_visitor()
    fw.visit(cv)
    content.fp = cv.fingerprint().compact()

    scep = int(content.metadata.get('scep'))
    content.template = 'spec'
    content.slug = 'scep%04d' % scep
    content.source_file = content.source_path.split('/')[-1]
    if scep > 0:
        content.status = 'hidden'
        content.title = content.slug.upper() + ' - ' + content.metadata.get('title')
    else:
        content.title = 'SCEPs'
        content.status = 'published'
    content.scep_status = content.metadata.get('status')
    content.scep_title = content.metadata.get('title')

    path = content.source_path
    status, stdout, stderr = git.execute(['git', 'ls-files', path, '--error-unmatch'],
            with_extended_output=True, with_exceptions=False)
    if status != 0:
        # file is not managed by git
        content.updated = time.gmtime(os.stat(path).st_mtime)
        content.gitrev = '(not yet committed)'
    else:
        commits = repo.iter_commits(paths=path)
	commit = commits.next()
        content.updated = datetime.fromtimestamp(commit.committed_date).timetuple()
        content.gitrev = commit.hexsha

    content.updated = time.strftime('%F %T UTC (%a, %d %B %Y)', content.updated)

def register():
    signals.content_object_init.connect(specs)
