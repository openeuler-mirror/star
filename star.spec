%global ALTERNATIVES    %{_sbindir}/alternatives
%global ALT_NAME        pax
%global ALT_LINK        %{_bindir}/pax
%global ALT_SL1_NAME    pax-man
%global ALT_SL1_LINK    %{_mandir}/man1/pax.1.gz
%global ALT_PATH        %{_bindir}/spax
%global ALT_SL1_PATH    %{_mandir}/man1/spax.1.gz

Name: star
Version: 1.6
Release: 4
Summary: An archiver supports ACL
License: CDDL
URL:     http://freecode.com/projects/%{name}
Source:  https://fossies.org/linux/misc/%{name}-%{version}.tar.bz2

Patch0:  star-1.6-star-mk.patch
Patch1:  star-1.5.2-bufferoverflow.patch
Patch2:  star-1.6-manpagereferences.patch
Patch3:  star-1.5.2-use-ssh-by-default.patch
Patch4:  bugfix-star-rmt-add-authority.patch

BuildRequires: libattr-devel libacl-devel libtool libselinux-devel e2fsprogs-devel git
Provides: scpio = %{version}-%{release} spax = %{version}-%{release} rmt = %{version}-%{release}
Obsoletes: scpio spax rmt 
Requires(post):  %{ALTERNATIVES}
Requires(preun): %{ALTERNATIVES}
Provides:        star-help = %{version}-%{release}
Obsoletes:       star-help < %{version}-%{release}

%description
Star is an archiver with ACL support, it saves many files together into a single
tape or disk archive, and can restore individual files from the archive.

%prep
%autosetup -n %{name}-%{version} -p1 -Sgit

cp -a star/all.mk star/Makefile

star_recode()
{
    for i in $@; do
        iconv -f iso_8859-1 -t utf-8 $i > .tmp_file
        mv .tmp_file $i
    done
}

star_recode AN-1.5 AN-1.5.2 star/star.4

for PLAT in %{arm} %{power64} aarch64 %{mips} x86_64 riscv64; do
    for AFILE in gcc cc; do
            [ ! -e RULES/${PLAT}-linux-${AFILE}.rul ] \
            && ln -s i586-linux-${AFILE}.rul RULES/${PLAT}-linux-${AFILE}.rul
    done
done

%build
%global make_flags GMAKE_NOWARN=true                                    \\\
    RUNPATH=                                                            \\\
    LDPATH=                                                             \\\
    PARCH=%{_target_cpu}                                                \\\
    K_ARCH=%{_target_cpu}                                               \\\
    INS_BASE=%{buildroot}%{_prefix}                                     \\\
    INS_RBASE=%{buildroot}                                              \\\
    INSTALL='sh $(SRCROOT)/conf/install-sh -c -m $(INSMODEINS)'         \\\
    COPTX="$RPM_OPT_FLAGS -DTRY_EXT2_FS"                                \\\
    LDOPTX="$RPM_LD_FLAGS"                                              \\\
    DEFCCOM=gcc

%make_build %make_flags

%install
make install -s %make_flags

ln -s star.1.gz %{buildroot}%{_mandir}/man1/ustar.1
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_pkgdocdir}
ln -s %{_sbindir}/rmt %{buildroot}%{_sysconfdir}/rmt
install -p -m 644 COPYING star/README  CDDL.Schily.txt AN-* %{buildroot}%{_pkgdocdir}

rm -rf %{buildroot}%{_prefix}/lib

%clean

%post
%{ALTERNATIVES} --install %{ALT_LINK} %{ALT_NAME} %{ALT_PATH} 66 \
    --slave %{ALT_SL1_LINK} %{ALT_SL1_NAME} %{ALT_SL1_PATH}

%preun
if [ $1 -eq 0 ]; then
    %{ALTERNATIVES} --remove %{ALT_NAME} %{ALT_PATH}
fi

%files
%exclude %{_bindir}/mt
%exclude %{_bindir}/smt
%exclude %{_bindir}/tartest
%exclude %{_bindir}/tar
%exclude %{_bindir}/gnutar
%exclude %{_bindir}/star_fat
%exclude %{_bindir}/star_sym
%exclude %{_bindir}/suntar
%exclude %{_sysconfdir}/default/star
%exclude %{_prefix}%{_sysconfdir}
%exclude %{_prefix}/include
%exclude %{_mandir}/man3
%exclude %{_mandir}/man5/{makefiles,makerules}.5*
%exclude %{_mandir}/man1/{tartest,gnutar,smt,mt,suntar,match}.1*
%exclude %{_docdir}/star/testscripts
%exclude %{_docdir}/star/TODO
%exclude %{_docdir}/rmt
%doc %{_pkgdocdir}
%{_bindir}/star
%{_bindir}/ustar
%dir %{_pkgdocdir}
%license COPYING
%doc %{_pkgdocdir}/CDDL.Schily.txt
%{_bindir}/scpio
%{_bindir}/spax
%ghost %verify(not md5 size mode mtime) %{ALT_LINK}
%ghost %verify(not md5 size mode mtime) %{ALT_SL1_LINK}
%{_sbindir}/rmt
%config %{_sysconfdir}/default/rmt
%{_sysconfdir}/rmt
%{_mandir}/man1/star*
%{_mandir}/man1/ustar.*
%{_mandir}/man5/star.*
%{_mandir}/man1/scpio.*
%{_mandir}/man1/spax.*
%{_mandir}/man1/rmt.*

%changelog
* Fri Dec 25 2020 Liquor<lirui130@huawei.com> -1.6-4
- add package star-help to package star

* Thu Sep 10 2020 wangchen<wangchen137@huawei.com> -1.6-3
- modify the URL of Source

* Wed Aug 26 2020 whoisxxx<zhangxuzhou4@huawei.com> -1.6-2
- Adapt to RISC-V

* Fri Aug 7 2020 Hugel<gengqihu1@huawei.com> -1.6-1
- update to 1.6

* Thu Nov 21 2019 fangyufa<fangyufa1@huawei.com> - 1.5.3-16
- add buildrequires of git for x86_64 build

* Mon Oct 21 2019 openEuler Buildteam<buildteam@openeuler.org> - 1.5.3-15
- Type:NA
- ID:NA
- SUG:NA
- DESC:Package Init
