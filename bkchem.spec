%define name 	bkchem
%define version 0.11.5
%define release %mkrel 1


Summary: 	Python 2D chemical structure drawing tool
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	http://www.zirael.org/bkchem/download/%name-%{version}.tar.bz2
URL: 		http://bkchem.zirael.org
License: 	GPL
Group: 		Sciences/Chemistry
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: 	python-devel 
Requires: 	python python-imaging Pmw PyXML
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
echo 'export BKCHEM_MODULE_PATH=%_libdir/python%pyver/site-packages/%name' >> $RPM_BUILD_ROOT/%_bindir/%name
echo 'export BKCHEM_TEMPLATE_PATH=%_datadir/%name/templates' >> $RPM_BUILD_ROOT/%_bindir/%name
echo 'export BKCHEM_PIXMAP_PATH=%_datadir/%name/pixmaps' >> $RPM_BUILD_ROOT/%_bindir/%name
echo 'export BKCHEM_IMAGE_PATH=%_datadir/%name/images' >> $RPM_BUILD_ROOT/%_bindir/%name
echo 'python %_libdir/python%pyver/site-packages/%name/%name.py' >> $RPM_BUILD_ROOT/%_bindir/%name
chmod 755 $RPM_BUILD_ROOT/%_bindir/%name

# menu
install -d $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):command="bkchem"\
needs="x11"\
section="More Applications/Sciences/Chemistry"\
title="BKChem"\
icon="chemistry_section.png"\
longtitle="2D chemical structure drawing tool" \
xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=BKchem
Comment=2D chemical structure drawing tool
Exec=bkchem
Icon=chemistry_section.png
Terminal=false
Type=Application
Categories=Science;Chemistry;X-MandrivaLinux-MoreApplications-Sciences-Chemistry;
EOF

%find_lang BKchem

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus

%postun
%clean_menus

%files -f BKchem.lang
%defattr(-,root,root)
%doc gpl.txt README RELEASE 
%_bindir/%name
%_datadir/%name
%doc %_docdir/%name
%_libdir/python%pyver/site-packages/%name
%_menudir/%name
%_datadir/applications/mandriva-%name.desktop

