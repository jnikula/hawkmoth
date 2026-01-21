Name:           hawkmoth
Version:        0.0.0
Release:        %autorelease
Summary:        Sphinx Autodoc for C

License:        BSD-2-Clause
URL:            https://github.com/jnikula/hawkmoth
Source:         %{pypi_source hawkmoth}
BuildArch:      noarch

BuildRequires:  python3-devel
# Clang python library dependency is not included in the pyproject.toml yet
BuildRequires:  python3-clang
Requires:       python3-clang
# Test dependencies. We cannot take them from pyproject.toml yet
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(strictyaml)

%description
Hawkmoth is a minimalistic Sphinx C and C++ Domain autodoc directive extension
to incorporate formatted C and C++ source code comments written in
reStructuredText into Sphinx based documentation. It uses Clang Python Bindings
for parsing, and generates C and C++ Domain directives for C and C++ API
documentation, and more. In short, Hawkmoth is Sphinx Autodoc for C/C++.


%prep
%autosetup


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l hawkmoth


%check
%pyproject_check_import
%pytest


%files -f %{pyproject_files}
%{_bindir}/hawkmoth
%doc README.rst CHANGELOG.rst


%changelog
%autochangelog
