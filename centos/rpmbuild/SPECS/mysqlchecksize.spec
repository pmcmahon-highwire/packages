Name:           mysqlchecksize
Version:        1.0.0
Release:        1%{?dist}
Summary:        mysqlchecksize is a utility that shows disk usage of mysql databases

Group:          Applications/System
License:        GPLv3
URL:            https://github.com/phayes/mysqlchecksize
Source0:        mysqlchecksize-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mercurial git golang


%description
mysqlchecksize is a utility that shows disk usage of mysql databases. It is installed on the mysql server machine that hosts the databases.
It can be run by any user and does not need special priviledges. 

%prep
rm -rf %{_tmppath}/mysqlchecksize-gopath
%setup -q

%build
mkdir -p %{_tmppath}/mysqlchecksize-gopath/src
export GOPATH=%{_tmppath}/mysqlchecksize-gopath
cp -r vendor/* $GOPATH/src
go build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_bindir}/
cp %{name}-%{version} $RPM_BUILD_ROOT/%{_bindir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%attr(4755, mysql, mysql) %{_bindir}/%{name}


%changelog
* Fri Feb 19 2015 Patrick Hayes <patrick.d.hayes@gmail.com> - 1.0.0
- Initial version of the package