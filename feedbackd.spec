#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	Haptic/visual/audio feedback for GNOME
Summary(pl.UTF-8):	Dotykowe/wizualne/dźwiękowe informacje zwrotne dla GNOME
Name:		feedbackd
Version:	0.5.0
Release:	2
License:	GPL v3+ (daemon), LGPL v2.1+ (library)
Group:		Daemons
#Source0Download: https://source.puri.sm/Librem5/feedbackd/-/tags
Source0:	https://source.puri.sm/Librem5/feedbackd/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
# Source0-md5:	80be81e175fc73e6d9dfcce79b6cb6f7
Patch0:		%{name}-types.patch
URL:		https://source.puri.sm/Librem5/feedbackd
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.1}
BuildRequires:	glib2-devel >= 1:2.66
BuildRequires:	gmobile-devel >= 0.1.0
BuildRequires:	gobject-introspection-devel
BuildRequires:	gsound-devel
BuildRequires:	json-glib-devel >= 1.6.2
BuildRequires:	libgudev-devel >= 232
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 1.0.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	vala
Requires(post,postun):	glib2 >= 1:2.50.0
Requires:	gmobile >= 0.1.0
Requires:	libfeedback = %{version}-%{release}
Requires:	libgudev >= 232
Requires:	json-glib >= 1.6.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
feedbackd provides a DBus daemon (feedbackd) to act on events to
provide haptic, visual and audio feedback. It offers a library
(libfeedback) and GObject introspection bindings to ease using it from
applications.

%description -l pl.UTF-8
Pakiet feedbackd dostarcza demon DBus (feedbackd), reagujący na
zdarzenia w celu zapewnienia dotykowych, wizualnych i dźwiękowych
informacji zwrotnych do użytkownika. Oferuje bibliotekę (libfeedback)
oraz wiązania GObject, ułatwiające używanie go z poziomu aplikacji.

%package -n libfeedback
Summary:	GNOME Feedback library
Summary(pl.UTF-8):	Biblioteka GNOME Feedback
License:	LGPL v2.1+
Group:		Libraries
Requires:	glib2 >= 1:2.66
Suggests:	%{name} = %{version}-%{release}

%description -n libfeedback
GNOME Feedback library.

%description -n libfeedback -l pl.UTF-8
Biblioteka GNOME Feedback.

%package -n libfeedback-devel
Summary:	Header files for Feedback library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Feedback
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	libfeedback = %{version}-%{release}
Requires:	glib2-devel >= 1:2.66

%description -n libfeedback-devel
Header files for Feedback library.

%description -n libfeedback-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Feedback.

%package -n vala-libfeedback
Summary:	Vala API for Feedback library
Summary(pl.UTF-8):	API języka Vala do biblioteki API
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	libfeedback-devel = %{version}-%{release}
Requires:	vala

%description -n vala-libfeedback
Vala API for Feedback library.

%description -n vala-libfeedback -l pl.UTF-8
API języka Vala do biblioteki API.

%package -n libfeedback-apidocs
Summary:	API documentation for Feedback library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Feedback
License:	LGPL v2.1+
Group:		Documentation
BuildArch:	noarch

%description -n libfeedback-apidocs
API documentation for Feedback library.

%description -n libfeedback-apidocs -l pl.UTF-8
Dokumentacja API biblioteki Feedback.

%prep
%setup -q -n %{name}-v%{version}
%patch0 -p1

%build
%meson build \
	%{?with_apidocs:-Dgtk_doc=true} \
	-Dman=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libfeedback-0 $RPM_BUILD_ROOT%{_gidocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%post	-n libfeedback -p /sbin/ldconfig
%postun	-n libfeedback -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/fbcli
%attr(755,root,root) %{_bindir}/fbd-theme-validate
%attr(755,root,root) %{_libexecdir}/fbd-alert-slider
%attr(755,root,root) %{_libexecdir}/fbd-ledctrl
%attr(755,root,root) %{_libexecdir}/feedbackd
%{_datadir}/dbus-1/services/org.sigxcpu.Feedback.service
%{_datadir}/feedbackd
%{_datadir}/glib-2.0/schemas/org.sigxcpu.feedbackd.gschema.xml
%{systemduserunitdir}/fbd-alert-slider.service
/lib/udev/rules.d/90-feedbackd.rules
%{_mandir}/man1/fbcli.1*
%{_mandir}/man1/fbd-theme-validate.1*
%{_mandir}/man5/feedback-themes.5*
%{_mandir}/man8/feedbackd.8*

%files -n libfeedback
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfeedback-0.0.so.0
%{_libdir}/girepository-1.0/Lfb-0.0.typelib
%{_datadir}/dbus-1/interfaces/org.sigxcpu.Feedback.xml

%files -n libfeedback-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfeedback-0.0.so
%{_includedir}/libfeedback-0.0
%{_datadir}/gir-1.0/Lfb-0.0.gir
%{_pkgconfigdir}/libfeedback-0.0.pc

%files -n vala-libfeedback
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libfeedback-0.0.deps
%{_datadir}/vala/vapi/libfeedback-0.0.vapi

%if %{with apidocs}
%files -n libfeedback-apidocs
%defattr(644,root,root,755)
%{_gidocdir}/libfeedback-0
%endif
