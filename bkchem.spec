%define name 	bkchem
%define version 0.14.0
%define release %mkrel 0.pre2.1


Summary: 	Python 2D chemical structure drawing tool
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0:	http://bkchem.zirael.org/download/%name-%{version}-pre2.tar.gz
URL: 		http://bkchem.zirael.org
License: 	GPLv2+
Group: 		Sciences/Chemistry
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
%py_requires -d
Requires: 	python-imaging Pmw PyXML
Buildarch:	noarch

%description
BKChem is a free (as in free software :o) chemical drawing program. It was
conceived and written by Beda Kosata.  Supported file formats are SVG and CML.
The output looks best with the Adobe SVG viewer, but sodipodi and batik do a
reasonable job as well.

%prep 
%setup -q -n %name-%{version}-pre2
touch INSTALL.binary

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_bindir
touch $RPM_BUILD_ROOT/%_bindir/%name
python setup.py install --root=$RPM_BUILD_ROOT
chmod 644 gpl.txt README 
pushd $RPM_BUILD_ROOT/%_datadir
chmod 644 `find -type f`
chmod 755 `find -type d`
popd

rm -fr $RPM_BUILD_ROOT/%_prefix/doc/api

#fix executable
rm $RPM_BUILD_ROOT%_bindir/%name
echo '#!/bin/sh' > $RPM_BUILD_ROOT/%_bindir/%name
echo 'export BKCHEM_MODULE_PATH=%{py_puresitedir}/%name' >> $RPM_BUILD_ROOT/%_bindir/%name
echo 'export BKCHEM_TEMPLATE_PATH=%_datadir/%name/templates' >> $RPM_BUILD_ROOT/%_bindir/%name
echo 'export BKCHEM_PIXMAP_PATH=%_datadir/%name/pixmaps' >> $RPM_BUILD_ROOT/%_bindir/%name
echo 'export BKCHEM_IMAGE_PATH=%_datadir/%name/images' >> $RPM_BUILD_ROOT/%_bindir/%name
echo 'python %{py_puresitedir}/%name/%name.py' >> $RPM_BUILD_ROOT/%_bindir/%name
chmod 755 $RPM_BUILD_ROOT/%_bindir/%name


mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=BKchem
Comment=2D chemical structure drawing tool
Exec=bkchem
Icon=chemistry_section
Terminal=false
Type=Application
Categories=Science;Chemistry;
EOF

%find_lang BKChem

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files -f BKChem.lang
%defattr(-,root,root)
%doc gpl.txt README 
%_bindir/%name
%_datadir/%name
%{py_puresitedir}/%name
%_datadir/applications/mandriva-%name.desktop
%{py_puresitedir}/*.egg-info


%changelog
* Wed Mar 09 2011 Stéphane Téletchéa <steletch@mandriva.org> 0.14.0-0.pre2.1mdv2011.0
+ Revision: 643050
- Update to 0.14pre2
- Fix BKChem macro name for lang detection
- Update URL and description

* Sun Oct 31 2010 Funda Wang <fwang@mandriva.org> 0.13.0-3mdv2011.0
+ Revision: 590787
- rebuild for py2.7

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 0.13.0-2mdv2010.0
+ Revision: 436826
- rebuild

* Mon Feb 23 2009 Frederik Himpe <fhimpe@mandriva.org> 0.13.0-1mdv2009.1
+ Revision: 344283
- Update to new version 0.13.0

* Tue Feb 17 2009 Frederik Himpe <fhimpe@mandriva.org> 0.12.6-1mdv2009.1
+ Revision: 342150
- update to new version 0.12.6

* Thu Dec 25 2008 Adam Williamson <awilliamson@mandriva.org> 0.12.5-2mdv2009.1
+ Revision: 319048
- own site directory
- rebuild for python 2.6

* Thu Nov 27 2008 Funda Wang <fwang@mandriva.org> 0.12.5-1mdv2009.1
+ Revision: 307195
- update to new version 0.12.5

* Sat Oct 25 2008 Frederik Himpe <fhimpe@mandriva.org> 0.12.4-1mdv2009.1
+ Revision: 297162
- update to new version 0.12.4

* Fri Oct 10 2008 Frederik Himpe <fhimpe@mandriva.org> 0.12.3-1mdv2009.1
+ Revision: 291493
- update to new version 0.12.3

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0.12.2-2mdv2009.0
+ Revision: 266243
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sat May 31 2008 Funda Wang <fwang@mandriva.org> 0.12.2-1mdv2009.0
+ Revision: 213602
- New version 0.12.2

* Mon May 19 2008 Frederik Himpe <fhimpe@mandriva.org> 0.12.1-1mdv2009.0
+ Revision: 209171
- New version
- Adapt to new license policy

* Sun May 04 2008 Funda Wang <fwang@mandriva.org> 0.12.0-2mdv2009.0
+ Revision: 201061
- fix startup script

* Thu Dec 27 2007 Jérôme Soyer <saispo@mandriva.org> 0.12.0-1mdv2008.1
+ Revision: 138375
- Fix building under x86_64

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - kill hardcoded icon extension
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

  + Emmanuel Andry <eandry@mandriva.org>
    - New version
    - drop old menu


* Mon Sep 04 2006 Jerome Soyer <saispo@mandriva.org> 0.11.5-1mdv2007.0
- New release 0.11.5

* Fri Feb 24 2006 Austin Acton <austin@mandriva.org> 0.11.4-1mdk
- New release 0.11.4

* Fri Feb 17 2006 Austin Acton <austin@mandriva.org> 0.11.3-1mdk
- New release 0.11.3

* Mon Jan 16 2006 Austin Acton <austin@mandriva.org> 0.11.2-1mdk
- New release 0.11.2

* Mon Dec 05 2005 Lenny Cartier <lenny@mandriva.com> 0.11.1-1mdk
- 0.11.1

* Fri Sep 30 2005 Lenny Cartier <lenny@mandriva.com> 0.11.0-1mdk
- 0.11.0

* Thu Jul 14 2005 Austin Acton <austin@mandriva.org> 0.10.2-1mdk
- New release 0.10.2

* Thu Jun 30 2005 Lenny Cartier <lenny@mandriva.com> 0.10.1-1mdk
- 0.10.1

* Sun Jun 26 2005 Austin Acton <austin@mandriva.org> 0.10.0-1mdk
- New release 0.10.0

* Mon Dec 06 2004 Austin Acton <austin@mandrake.org> 0.9.0-1mdk
- 0.9.0
- source URL

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 0.8.1-2mdk
- Rebuild for new python
- various spec fix

* Fri Oct 08 2004 Austin Acton <austin@mandrake.org> 0.8.1-1mdk
- 0.8.1

* Mon Oct 04 2004 Austin Acton <austin@mandrake.org> 0.8.0-1mdk
- 0.8.0 final

* Thu Aug 26 2004 Austin Acton <austin@mandrake.org> 0.8.0-0.pre1.1mdk
- 0.8.0pre1

* Fri Aug 20 2004 Austin Acton <austin@mandrake.org> 0.7.1-2mdk
- new menu

* Wed Aug 11 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.7.1-1mdk
- 0.7.1

* Mon Aug 09 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.7.0-1mdk
- 0.7.0

* Sun May 02 2004 Austin Acton <austin@mandrake.org> 0.6.0-1mdk
- 0.6.0

* Mon Mar 01 2004 Austin Acton <austin@mandrake.org> 0.5.2-1mdk
- 0.5.2

* Wed Feb 25 2004 Austin Acton <austin@mandrake.org> 0.5.1-1mdk
- 0.5.1

* Mon Feb 16 2004 Austin Acton <austin@mandrake.org> 0.5.1-0.pre1.1mdk
- 0.5.1pre1

* Tue Sep 30 2003 Austin Acton <aacton@yorku.ca> 0.5.0-1mdk
- 0.5.0 final

