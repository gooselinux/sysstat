Name: sysstat
Version: 9.0.4
Release: 12%{?dist}.1
Summary: The sar and iostat system monitoring commands
License: GPLv2+
Group: Applications/System
URL: 	http://perso.orange.fr/sebastien.godard/
Source: http://perso.orange.fr/sebastien.godard/%{name}-%{version}.tar.bz2
# fix initscript
Patch0: sysstat-9.0.4-init_script.patch
# fixes https://bugzilla.redhat.com/show_bug.cgi?id=545931
Patch1: sysstat-9.0.4-nfs.patch
# make init script lsb
Patch2: sysstat-9.0.4-init_script_lsb.patch
Patch3: sysstat-9.0.4-tickless.patch
# fixes 579084 - svctm field has no sense
Patch4: sysstat-9.0.4-svctm.patch
# fixes 600275 - The 'sar -d ' command outputs invalid data
Patch5: sysstat-9.0.4-cntrwrap.patch
Patch6: sysstat-9.0.6.1-sec.patch
Patch7: sysstat-9.0.4-intr.patch
Patch8: sysstat-9.0.4-cpu.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 

Requires: /sbin/chkconfig
Requires: sh-utils textutils grep fileutils /etc/cron.d
BuildRequires: perl %{_includedir}/linux/if.h gettext
Requires: %__cp %__mv %__chmod %__grep %__mkdir %__install %__id

%description
This package provides the sar and iostat commands for Linux. Sar and
iostat enable system monitoring of disk, network, and other IO
activity.

%prep
%setup -q
%patch0 -p1 -b .ii
%patch1 -p1 -b .nfs
%patch2 -p1 -b .lsb
%patch3 -p1 -b .tl
%patch4 -p1 -b .svctm
%patch5 -p1 -b .over
%patch6 -p1 -b .sec
%patch7 -p1 -b .intr
%patch8 -p1 -b .cpu
iconv -f windows-1252 -t utf8 CREDITS > CREDITS.aux
mv CREDITS.aux CREDITS

%build
# FIXME: I need to fix the upstream Makefile to use LIBDIR et al. properly and
# send the upstream maintainer a patch.
# add DOCDIR to the configure part
./configure --disable-man-group --prefix=%{_prefix} --mandir=%{_mandir} sa_lib_dir=%{_libdir}/sa --libdir=%{_libdir}
CFLAGS="$RPM_OPT_FLAGS -DSADC_PATH=\\\"%{_libdir}/sa/sadc\\\""
make CFLAGS="$CFLAGS" LFLAGS="" DOC_DIR=%{_docdir}/%{name}-%{version}

%install
rm -rf %{buildroot}

make install IGNORE_MAN_GROUP=y DOC_DIR=%{_docdir}/%{name}-%{version} INIT_DIR=%{_initrddir}

mkdir -p %{buildroot}/%{_sysconfdir}/cron.d
install -m 0644 sysstat.crond %{buildroot}/%{_sysconfdir}/cron.d/sysstat
mkdir -p %{buildroot}%{_initrddir}
install -m 0755 sysstat %{buildroot}%{_initrddir}/

%find_lang %{name}

%post
/sbin/chkconfig --add sysstat

%preun
if [ "$1" = 0 ]; then
  # Remove sa logs if removing sysstat completely
  rm -f %{_localstatedir}/log/sa/*
  # Remove service
  /sbin/chkconfig --del sysstat
fi

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc CHANGES COPYING CREDITS README TODO FAQ
%config(noreplace) %{_sysconfdir}/cron.d/sysstat
%config(noreplace) %{_sysconfdir}/sysconfig/sysstat
%config(noreplace) %{_sysconfdir}/sysconfig/sysstat.ioconf
%{_initrddir}/sysstat
%{_bindir}/*
%{_libdir}/sa
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_localstatedir}/log/sa

%changelog
* Wed Nov 10 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.4-12.1
- Resolves: #651813
  mpstat problem with cpu_usr, cpu_guest values

* Fri Nov  5 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.4-11.1
- Resolves: #650125
  mpstat -I ALL displays incorrect values

* Mon Jul 26 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.4-11
- Resolves: #615234
  sysstat not monitor system every second

* Thu Jun 17 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.4-10
- Resolves: #600275
  The 'sar -d ' command outputs invalid data

* Tue Jun  1 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.4-9
- Resolves: #579084
  The calculation of svctm is incorrect

* Mon Apr 19 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.4-8
- Related: #536928
  fix the output of mpstat for cpu which are switched off

* Fri Apr 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.4-7
- Resolves: #536928
  fix the mpstat output on tickless kernel

* Tue Feb 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.4-6
- Related: #543948
  fix init script format

* Thu Dec 10 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 9.0.4-5
- fix the problem in get_nfs_mount_nr function
  ( iostat -n causes stack smashing)

* Tue Sep 15 2009 Ivana Varekova <varekova@redhat.com> - 9.0.4-4
- fix init script

* Mon Sep 14 2009 Ivana Varekova <varekova@redhat.com> - 9.0.4-3
- fix init script - add INIT INFO flags (#522740)
  and add condrestart, try-restart and force-reload (#522743)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Ivana Varekova <varekova@redhat.com> - 9.0.4-1
- update to 9.0.4

* Thu May 28 2009 Ivana Varekova <varekova@redhat.com> - 9.0.3-1
- update to 9.0.3
- remove obsolete patches

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-6
- add /proc/diskstats reading patch

* Mon Sep 22 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-5
- Resolves: #463066 - Fix Patch0:/%%patch mismatch

* Wed Apr 23 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-4 
- Resolves: #442801 mpstat shows one extra cpu
  thanks Chris Wright

* Thu Mar  6 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-3
- add nfs extended statistic to iostat command

* Thu Feb 28 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-2
- retry write functuon in sadc command - thanks Tomas Mraz

* Fri Feb  8 2008 Ivana Varekova <varekova@redhat.com> - 8.0.4-1
- updated to 8.0.4

* Mon Dec  3 2007 Ivana Varekova <varekova@redhat.com> - 8.0.3-1
- updated to 8.0.3

* Fri Nov  9 2007 Ivana Varekova <varekova@redhat.com> - 8.0.2-3
- used macros instead of var, etc 

* Thu Nov  8 2007 Ivana Varekova <varekova@redhat.com> - 8.0.2-2
- change license tag
- remove sysstat.crond source (add -d)
- remove obsolete sysconfig file
- spec file cleanup

* Mon Nov  5 2007 Ivana Varekova <varekova@redhat.com> - 8.0.2-1
- update 8.0.2
- spec file cleanup

* Wed Oct 24 2007 Ivana Varekova <varekova@redhat.com> - 8.0.1-2
- remove useless patches

* Mon Oct 22 2007 Ivana Varekova <varekova@redhat.com> - 8.0.1-1
- update to 8.0.1
- remove useless patches
- spec file cleanup
- remove smp build flag (ar problem)
- add libdir flags 

* Wed Aug 15 2007 Ivana Varekova <varekova@redhat.com> - 7.0.4-3
- fix cve-2007-3852 -
  sysstat insecure temporary file usage

* Fri Mar 23 2007 Ivana Varekova <varekova@redhat.com> - 7.0.4-2
- fix sa2 problem (sa2 works wrong when the /var/log/sa file is 
  a link to another directory)

* Mon Feb 12 2007 Ivana Varekova <varekova@redhat.com> - 7.0.4-1
- update to 7.0.4
- spec file cleanup

* Tue Jan 30 2007 Ivana Varekova <varekova@redhat.com> - 7.0.3-3
- remove -s flag

* Mon Dec 18 2006 Ivana Varekova <varekova@redhat.com> - 7.0.3-1
- update to 7.0.3

* Tue Nov 21 2006 Ivana Varekova <varekova@redhat.com> - 7.0.2-3
- update NFS mount statistic patch 

* Wed Nov  8 2006 Ivana Varekova <varekova@redhat.com> - 7.0.2-1
- update to 7.0.2

* Thu Oct 26 2006 Ivana Varekova <varekova@redhat.com> - 7.0.0-3
- move tmp file (#208433)

* Mon Oct  9 2006 Ivana Varekova <varekova@redhat.com> - 7.0.0-2
- add NFS mount statistic (#184321)

* Fri Jul 14 2006 Marcela Maslanova <mmaslano@redhat.com> - 7.0.0-1
- new version 7.0.0

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.0.2-2.1
- rebuild

* Mon Jun  5 2006 Jesse Keating <jkeating@redhat.com> 6.0.2-2
- Add missing BR of gettext

* Fri May  5 2006 Ivana Varekova <varekova@redhat.com> 6.0.2-1
- update to 6.0.2
- remove asm/page.h used sysconf command to get PAGE_SIZE

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.0.1-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.0.1-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Oct 11 2005 Ivana Varekova <varekova@redhat.com> 6.0.1-3
- add FAQ to documentation (bug 170158)

* Mon Oct 10 2005 Ivana Varekova <varekova@redhat.com> 6.0.1-2
- fix chkconfig problem

* Fri Oct  7 2005 Ivana Varekova <varekova@redhat.com> 6.0.1-1
- version 6.0.1

* Thu Aug 18 2005 Florian La Roche <laroche@redhat.com>
- no need to kernel kernel 2.2 or newer anymore

* Tue May 10 2005 Ivana Varekova <varekova@redhat.com> 5.0.5-10.fc
- add debug files to debug_package

* Mon Mar  7 2005 Ivana Varekova <varekova@redhat.com> 5.0.5-9.fc
- rebuilt (add gcc4fix, update lib64ini)

* Fri Mar  4 2005 Ivana Varekova <varekova@redhat.ccm> 5.0.5-7.fc
- rebuilt

* Thu Sep 30 2004 Charles Bennett <ccb@redhat.com> 5.0.5-5.fc
- bring in filename and append-msg patch
- append-msg adds verbose text for when saNN data file cpu count
-  does not match cpu count on the currently running system

* Wed Jun 30 2004 Nils Philippsen <nphilipp@redhat.com>
- version 5.0.5
- remove some obsolete patches
- update statreset, overrun, lib64init patches
- renumber patches

* Wed Jun 16 2004 Alan Cox <alan@redhat.com>
- Fix spew of crap to console at startup
- Fix order of startup (#124035)
- Fix array overrun (#117182)
- Fix interrupt buffer sizing (caused bogus irq info)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 24 2004 Justin Forbes <64bit_fedora@comcast.net> 5.0.1-2
- fix lib64 init

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 18 2004 Nils Philippsen <nphilipp@redhat.com> 5.0.1-1
- version 5.0.1
- update statreset patch

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 22 2004 Nils Philippsen <nphilipp@redhat.com> 5.0.0-0.6
- let user configure how long to keep logs through /etc/sysconfig/sysstat
  (#81294)
- reset stats at system boot (#102445)

* Wed Jan 21 2004 Nils Philippsen <nphilipp@redhat.com> 5.0.0-0.5
- fix ifnamsiz patch for s390x (hopefully)

* Tue Jan 20 2004 Nils Philippsen <nphilipp@redhat.com> 5.0.0-0.4
- fix insecure tmp files in scripts (#78212)
- require tools needed in scripts
- use IFNAMSIZ from {_includedir}/linux/if.h for maximum interface length

* Mon Jan 12 2004 Nils Philippsen <nphilipp@redhat.com> 5.0.0-0.3
- Buildrequires: perl
- check for %%_lib == lib64 instead of specific arches

* Mon Jan 12 2004 Nils Philippsen <nphilipp@redhat.com> 5.0.0-0.2
- fix dealing with lib64 case of cron.d file

* Mon Jan 12 2004 Nils Philippsen <nphilipp@redhat.com> 5.0.0-0.1
- version 5.0.0

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Mar  3 2003 Joe Orton <jorton@redhat.com> 4.0.7-4
- really fix paths for multilib (#82913)

* Wed Feb 19 2003 Bill Nottingham <notting@redhat.com> 4.0.7-3
- fix paths on multilib arches (#82913)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Nov 23 2002 Mike A. Harris <mharris@redhat.com> 4.0.7-1
- Updated to new upstream version 4.0.7

* Tue Nov 19 2002 Mike A. Harris <mharris@redhat.com> 4.0.5-7
- Fixed files installed in /usr/doc to be put in correct place

* Tue Oct  8 2002 Mike A. Harris <mharris@redhat.com> 4.0.5-6
- All-arch rebuild

* Tue Jul 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.5-3
- Rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 17 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.5-1
- 4.0.5-1
- isag is no longer installed by default upstream, removing
  requirement on gnuplot

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 22 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.4-1
- 4.0.4
- Add an explicit requires on gnuplot (#63474)

* Fri Apr 12 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.3-2
- Do the daily sa2 run just before midnight, not at 4AM... you'd 
  only get 4 hours worth of data that way (#63132)

* Thu Feb 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.3-1
- 4.0.3

* Wed Feb 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.2-3
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Dec 12 2001 Trond Eivind Glomsrød <teg@redhat.com> 4.0.2-1
- 4.0.2
- the kernel patch for extended statistics is in, don't say it needs
  applying in the man page

* Mon Aug 13 2001 Preston Brown <pbrown@redhat.com>
- be more verbose about which files are corrupt (#47122)

* Mon Jul  2 2001 Preston Brown <pbrown@redhat.com>
- run sa1 from cron.d to fix run-parts interaction problem (#37733)

* Fri Jun 29 2001 Preston Brown <pbrown@redhat.com>
- upgrade to 4.0.1 stable release

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Sun Apr  8 2001 Preston Brown <pbrown@redhat.com>
- explicitly set safe umask (#35142)

* Fri Mar  9 2001 Preston Brown <pbrown@redhat.com>
- iostat disk utilization was off by a factor of 10.

* Wed Feb 14 2001 Preston Brown <pbrown@redhat.com>
- 3.3.5 brings us full support for kernel IO stats

* Tue Jan 30 2001 Preston Brown <pbrown@redhat.com>
- Summarize previous day's activity with sa2, not current day (which is only 4 hours of data when it gets run) (#24820)
- upgrade to 3.3.4 for full 2.4 compatibility and improved iostat

* Tue Jan 17 2001 Preston Brown <pbrown@redhat.com>
- iostat man page fixes

* Fri Jan 05 2001 Preston Brown <pbrown@redhat.com>
- 3.3.3, crontab fixes

* Fri Dec 29 2000 Bill Nottingham <notting@redhat.com>
- fix prereqs

* Fri Oct 13 2000 Preston Brown <pbrown@redhat.com>
- crontab entry was still incorrect.  Fixed.

* Mon Oct 09 2000 Preston Brown <pbrown@redhat.com>
- make sure disk accounting is enabled to fix iostat -l, -p (#16268)
- crontab entries were missing the user (root) to run as (#18212)

* Tue Aug 22 2000 Preston Brown <pbrown@redhat.com>
- enable IO accounting now that kernel supports it

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix buildrooting (#16271)

* Tue Aug 08 2000 Preston Brown <pbrown@redhat.com>
- bugfixes in 3.2.4 cause our inclusion. :)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 29 2000 Preston Brown <pbrown@redhat.com>
- 3.2.3 fixes SMP race condition

* Tue Jun 20 2000 Preston Brown <pbrown@redhat.com>
- FHS macros
- 3.2.2

* Fri May 26 2000 Preston Brown <pbrown@redhat.com>
- packaged for Winston
- change va patch to indicate kernel is not patched for iostat accounting.
  re-enable if our stock kernel gets this patch.
- upgrade to 3.2.
- install crontab entry.

* Sun Dec 12 1999  Ian Macdonald <ian@caliban.org>
- upgraded to 2.2

* Fri Oct 29 1999  Ian Macdonald <ian@caliban.org>
- first RPM release (2.1)
