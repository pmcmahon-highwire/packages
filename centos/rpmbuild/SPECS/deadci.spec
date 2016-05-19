Name:             deadci
Version:          1.0.0
Release:          1%{?dist}
Summary:          DeadCI is a lightweight continuous integration and testing web server.

Group:            Applications/System
License:          GPLv3
URL:              https://deadci.com/
Requires(pre):    /usr/sbin/useradd, /usr/bin/getent
Requires(postun): /usr/sbin/userdel
Source0:          https://github.com/phayes/packages/blob/master/centos/rpmbuild/SOURCES/%{name}-%{version}.tar.gz
Source1:          https://github.com/phayes/packages/blob/master/centos/rpmbuild/SOURCES/deadci.init
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  mercurial git
BuildRequires:  golang >= 1.5


%description
DeadCI is a lightweight continuous integration and testing web server that integrates seamlessly with GitHub (other platforms coming). As the name implies it is dead easy to use. DeadCI works by running a command of your choice at the root of the repository being built. It's easy to run TravisCI jobs from a .travis.yml locally. It also integrates nicely with JoliCI to run yours tests inside a Docker container.

%prep
rm -rf %{_tmppath}/deadci-gopath
%setup -q

%build
mkdir -p %{_tmppath}/deadci-gopath/src
export GOPATH=%{_tmppath}/deadci-gopath
cp -r vendor/* $GOPATH/src
go build

%pre
/usr/bin/getent group deadci || /usr/sbin/groupadd -r deadci
/usr/bin/getent passwd deadci || /usr/sbin/useradd -r -d /var/lib/deadci -s /sbin/nologin deadci

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_bindir}/
mkdir -p $RPM_BUILD_ROOT/etc/deadci
mkdir -p $RPM_BUILD_ROOT/var/lib/deadci
mkdir -p $RPM_BUILD_ROOT/etc/init.d
cp %{name}-%{version} $RPM_BUILD_ROOT/%{_bindir}/%{name}
cp deadci.ini $RPM_BUILD_ROOT/etc/deadci
cp %{SOURCE1} $RPM_BUILD_ROOT/etc/init.d/deadci

%post
/sbin/chkconfig --add %{name}

%preun
%{_initrddir}/%{name} stop >/dev/null 2>&1
/sbin/chkconfig --del %{name}

%postun
/usr/sbin/userdel deadci

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,deadci,deadci,-)
%doc README.md
%attr(4755, deadci, deadci) %{_bindir}/%{name}
%attr(755, root, root) /etc/init.d/deadci
%dir /etc/deadci
%config(noreplace) /etc/deadci/deadci.ini
%dir /var/lib/deadci


%changelog
* Mon May 16 2015 Patrick Hayes <patrick.d.hayes@gmail.com> - 1.0.0
- Initial version of the package
