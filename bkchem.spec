%define name 	bkchem
%define version 0.14.0
%define release %mkrel 0.pre2.2


Summary: 	Python 2D chemical structure drawing tool
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0:	http://bkchem.zirael.org/download/%name-%{version}-pre2.tar.gz
URL: 		http://bkchem.zirael.org
License: 	GPLv2+
Group: 		Sciences/Chemistry
BuildRequires:	python-devel
Requires: 	python-imaging Pmw
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
rm -rf %{buildroot}
mkdir -p %{buildroot}/%_bindir
touch %{buildroot}/%_bindir/%name
python setup.py install --root=%{buildroot}
chmod 644 gpl.txt README 
pushd %{buildroot}/%_datadir
chmod 644 `find -type f`
chmod 755 `find -type d`
popd

rm -fr %{buildroot}/%_prefix/doc/api

#fix executable
rm %{buildroot}%_bindir/%name
echo '#!/bin/sh' > %{buildroot}/%_bindir/%name
echo 'export BKCHEM_MODULE_PATH=%{py_puresitedir}/%name' >> %{buildroot}/%_bindir/%name
echo 'export BKCHEM_TEMPLATE_PATH=%_datadir/%name/templates' >> %{buildroot}/%_bindir/%name
echo 'export BKCHEM_PIXMAP_PATH=%_datadir/%name/pixmaps' >> %{buildroot}/%_bindir/%name
echo 'export BKCHEM_IMAGE_PATH=%_datadir/%name/images' >> %{buildroot}/%_bindir/%name
echo 'python %{py_puresitedir}/%name/%name.py' >> %{buildroot}/%_bindir/%name
chmod 755 %{buildroot}/%_bindir/%name

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
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

%files -f BKChem.lang
%doc gpl.txt README 
%_bindir/%name
%_datadir/%name
%{py_puresitedir}/%name
%_datadir/applications/mandriva-%name.desktop
%{py_puresitedir}/*.egg-info
