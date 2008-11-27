%define name 	bkchem
%define version 0.12.5
%define release %mkrel 1


Summary: 	Python 2D chemical structure drawing tool
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	http://www.zirael.org/bkchem/download/%name-%{version}.tar.gz
URL: 		http://bkchem.zirael.org
License: 	GPLv2+
Group: 		Sciences/Chemistry
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
%py_requires -d
Requires: 	python-imaging Pmw PyXML
Buildarch:	noarch

%description
BKchem is a free (as in free software :o) chemical drawing program. It was
concieved and written by Beda Kosata.  Supported file formats are SVG and CML.
The output looks best with the Adobe SVG viewer, but sodipodi and batik do a
reasonable job as well.

%prep
%setup -q
touch INSTALL.binary

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_bindir
touch $RPM_BUILD_ROOT/%_bindir/%name
python setup.py install --root=$RPM_BUILD_ROOT
chmod 644 gpl.txt README RELEASE
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

%find_lang BKchem

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

%files -f BKchem.lang
%defattr(-,root,root)
%doc gpl.txt README RELEASE
%_bindir/%name
%_datadir/%name
%{py_puresitedir}/%name/*
%_datadir/applications/mandriva-%name.desktop
%{py_puresitedir}/*.egg-info
