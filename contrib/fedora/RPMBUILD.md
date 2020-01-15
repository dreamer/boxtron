Prepare rpmbuild tree:

    $ rpmdev-setuptree

Build rpm and srpm using specfile and auto-downloaded sources:

    $ cp boxtron.spec ~/rpmbuild/SPECS/
    $ cd ~/rpmbuild/SPECS/
    $ spectool -g -R boxtron.spec
    $ rpmbuild -bb boxtron.spec
    $ rpmbuild -bs boxtron.spec

Build local tag using an archive generated locally:

    $ git archive --format=tar --prefix=boxtron-0.5.4/ v0.5.4^{tree} | gzip >boxtron-0.5.4.tar.gz
    $ mv boxtron-0.5.4.tar.gaz ~/rpmbuild/SOURCES/
    
    edit Version, Release fields and changelog in boxtron.spec file
    
    $ cd ~/rpmbuild/SPECS/
    $ rpmbuild -bb boxtron.spec
    $ rpmbuild -bs boxtron.spec

Do some verification:

    $ rpmlint ~/rpmbuild/RPMS/noarch/boxtron-0.5.4*
    $ rpmlint ~/rpmbuild/SRPMS/boxtron-0.5.4*

To publish on copr:

1. Upload srpm to public location (bender?)
2. Open copr boxtron page, switch to "Builds" tab
3. Click "New Build", select "From URLs"
4. Paste public URL pointing to srpm
5. Click "Build"
