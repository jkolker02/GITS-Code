clear,clc,close all

tic;
FolderList = dir('C:\Users\jack.kolker\Desktop\Summer 2022\Code\Test Logs');
FolderList = FolderList([FolderList.isdir]);
FolderList(2) = [];
FolderList(1) = [];

files = dir(fullfile('C:\Users\jack.kolker\Desktop\Summer 2022\Code\Test Logs', FolderList(1).name));
files2 = dir(fullfile('C:\Users\jack.kolker\Desktop\Summer 2022\Code\Test Logs', FolderList(2).name));


files(2) = [];
files(1) = [];

files2(2) = [];
files2(1) = [];

counter = 0;
  
#------Cylinder Posclition vs Time graph------
#
maxs = zeros(size(files));
f1 = figure('Name', "Cylinder Position vs Time", 'NumberTitle', 'off');#'Position', [2500 250 550 500]);
for index = 1:size(files)(1)
  subplot(2,1,1)
  filename = strcat('Compressive Logs/',files(index).name);
  plot(load(filename)(:,1),load(filename)(:,2)*33.4);
  hold on
  maxs(index) = max(load(filename)(:,2));
  counter += size(load(filename)(:,1),1);
end
title("Cylinder Position vs Time (COMPRESSIVE)");
xlabel("Time (s)");
ylabel("Position (deg)");
hold off


maxs2 = zeros(size(files2));
for index = 1:size(files2)(1)
  subplot(2,1,2)
  filename = strcat('Orbital Logs/',files2(index).name);
  plot(load(filename)(:,1),load(filename)(:,2)*33.4);
  hold on
  maxs2(index) = max(load(filename)(:,2));
  counter += size(load(filename)(:,1),1);
end
title("Cylinder Position vs Time (ORBITAL)");
xlabel("Time (s)");
ylabel("Position (deg)");
hold off

disp('Fig1[DONE]')

#------Torque vs Time graph------
#
f2 = figure('Name', "Torque vs Time", 'NumberTitle', 'off');# 'Position', [3100 250 550 500]);
maxsT = zeros(size(files));
for index = 1:size(files)(1)
  subplot(2,1,1)
  filename = strcat('Compressive Logs/', files(index).name);
  plot(load(filename)(:,1),load(filename)(:,3)*23.6);
  hold on
  maxsT(index) = max(load(filename)(:,3));
  counter += size(load(filename)(:,1),1);
end
title("Torque vs Time (COMPRESSIVE)");
xlabel("Time (s)");
ylabel("Torque (Ft-Lbs)");


maxsT2 = zeros(size(files2));
for index = 1:size(files2)(1)
  subplot(2,1,2)
  filename = strcat('Orbital Logs/', files2(index).name);
  plot(load(filename)(:,1),load(filename)(:,3)*23.6);
  hold on
  maxsT2(index) = max(load(filename)(:,3));
  counter += size(load(filename)(:,1),1);
end
title("Torque vs Time (ORBITAL)");
xlabel("Time (s)");
ylabel("Torque (Ft-Lbs)");
hold off

disp('Fig2[DONE]')

#------Angle Transducer 2 vs Time------
#
f3 = figure('name', 'Angle 2 vs Time', 'NumberTitle', 'off');# 'Position', [2500 -400 550 500]);
maxsA = zeros(size(files));

for index = 1:size(files)(1)
  subplot(2,1,1)
  filename = strcat('Compressive Logs/', files(index).name);
  base = load(filename)(3,5)*33.4; #CHANGE TO 33.4 WITH NEW ANGLE TRANSDUCER
  ang2 = load(filename)(:,5)*33.4;
  ang2 = ang2 - base;
  plot(load(filename)(:,1),ang2);
  hold on
  maxsA(index) = max(load(filename)(:,5));
  counter += size(load(filename)(:,1),1);
end
title("Angle Transducer 2 Position vs Time (COMPRESSIVE)");
xlabel("Time (s)");
ylabel("Position (deg)");
hold off

maxsA2 = zeros(size(files2));
for index = 1:size(files2)(1)
  subplot(2,1,2)
  filename = strcat('Orbital Logs/', files2(index).name);
  base = load(filename)(3,5)*33.4;#CHANGE TO 33.4 WITH NEW ANGLE TRANSDUCER
  ang2 = load(filename)(:,5)*33.4;
  ang2 = ang2 - base;
  plot(load(filename)(:,1),ang2);
  hold on
  maxsA2(index) = max(load(filename)(:,5));
  counter += size(load(filename)(:,1),1);
end
title("Angle Transducer 2 Position vs Time (ORBITAL)");
xlabel("Time (s)");
ylabel("Position (deg)");
hold off

disp('Fig3[DONE]')

#------Torque vs Displacement------
#
yields = [];
f4 = figure('name', 'Torque vs Angular Displacement', 'NumberTitle','off');# 'Position', [3100 -400 550 500]);
for index = 1:size(files)(1)
  filename = strcat('Compressive Logs/', files(index).name);
  base = load(filename)(3,5)*33.4; #CHANGE TO 33.4 WITH NEW ANGLE TRANSDUCER
  ang2 = load(filename)(:,5)*33.4;
  ang2 = abs(ang2 - base);
  torque = load(filename)(:,3)*23.6;
  p1 = plot(ang2,torque,'r', 'LineWidth', 3);
  hold on
%  if (ang2(1000) == ang2(150))
%    slope = (torque(1200)-torque(400))/(ang2(1200)-ang2(400));
%    disp('1');
%  else 
%    slope = (torque(1200) - torque(400))/(ang2(1200)-ang2(400));
%  end
%  x = linspace(0,15,1000);
%  y = slope*x;
  #plot(x,y);
  hold on
  run = true;
  
%  for i = 1000:size(torque)(1)
%    counter = counter + 1;
%    tor = torque(i);
%    a = ang2(i);
%    if ((abs(tor - (a*slope))) > 8 && run == true && tor > 35)
%      yields(length(yields)+1) = tor;
%      run = false;
%    end
%  end
%  a = 30/57.2;
%  z = a;
%  b = -.1145915 * slope - (z*slope);
%  y2 = slope * x + fb;
%  #plot(x, y2);
  hold on
  counter += size(load(filename)(:,1),1);
end
yields
title("Torque vs  Angular Displacement");
xlabel('Angular Displacement (deg)')
ylabel('Torque (Ft-Lbs)')
hold on

for index = 1:size(files2)(1)
  filename = strcat("Orbital Logs/", files2(index).name);
  base = load(filename)(3,5)*33.4; #CHANGE TO 33.4 WITH NEW ANGLE TRANSDUCER
  ang2 = load(filename)(:,5)*33.4;
  ang2 = abs(ang2 - base);
  p2 =plot(ang2,load(filename)(:,3)*23.6,'b','LineWidth', 1);
  hold on
  counter += size(load(filename)(:,1),1);
end
hold on
#legend([p1,p2],{'Compressive','Orbital'})

disp('Fig4[DONE]')


for index= 1:size(maxsT)
  name = files(index).name;
  str = strcat(name, '-', num2str(maxsT(index)*23.6));
  disp(str);
end

  



#--------DISPLAY DATA--------
#
disp('------------------------------------------');
disp('|~~~~~~~~~~~~~~Data Analysis~~~~~~~~~~~~~~|');
disp('------------------------------------------');

#-----Max Position Data-----
#
disp('');
disp('--------------------');
disp('Average Max Position');
disp('--------------------');
avgmax = sum(maxs)/size(maxs,1);
avgmax2 = sum(maxs2)/size(maxs2,1);
str1 = sprintf("Comp: %d", avgmax*33.4);
str12 = sprintf("Orbt: %d", avgmax2*33.4);
cstd = std(maxs);
ostd = std(maxs2);
str131 = sprintf("std dev: %d", cstd);
str132 = sprintf('std dev: %d', ostd);
disp(str1);
disp(str131);
disp("")
disp(str12);
disp(str132);


#-----Max Torque Data-----
#
disp('')
disp('--------------------------');
disp('Average Max Torque Applied');
disp('--------------------------');
avgmaxT = sum(maxsT)/size(maxsT,1);
avgmaxT2 = sum(maxsT2)/size(maxsT2,1);
str2 = sprintf("Comp: %d", avgmaxT*23.6032);
str22 = sprintf("Orbt: %d", avgmaxT2*23.6032);
ctstd = std(maxsT);
otstd = std(maxsT2);
str231 = sprintf("std dev: %d", ctstd);
str232 = sprintf('std dev: %d', otstd);
str241 = '';
if (avgmaxT > avgmaxT2)
  str241 = sprintf('C > O by: %d', (avgmaxT - avgmaxT2)*23.6032);
end
if (avgmaxT2 > avgmaxT)
  str241 = sprintf('O > C by: %d', (avgmaxT2 - avgmaxT)*23.6032);
end
disp(str2);
disp(str231);
disp("");
disp(str22);
disp(str232);
disp('');
disp(str241);

#-----Max Angle2 Data-----
#
disp('')
disp('----------------------------');
disp('Average Max Angle 2 Position');
disp('----------------------------');
avgmaxA=sum(maxsA)/size(maxsA,1);
avgmaxA2 = sum(maxsA2)/size(maxsA2,1);
str3 = sprintf('Comp: %d', avgmaxA*4.5);
str32 = sprintf('Orbt: %d', avgmaxA2*4.5);
castd = std(maxsA);
oastd = std(maxsA2);
str331 = sprintf("std dev: %d", castd);
str332 = sprintf("std dev: %d", oastd);
disp(str3);
disp(str331);
disp('')
disp(str32);
disp(str332);
                

#------Runtime Stats------
#
disp('')
disp('------------------')
disp('Runtime Statistics')
disp('------------------')
str4 = sprintf('n = %d', counter);
t = toc;
str5 = sprintf('Runtime = %d sec', (t));
str6 = sprintf('Ops/S: %d', (counter / t));
str7 = strcat('Directory Comp: ', fullfile(' C:\Users\jack.kolker\Desktop\Summer 2022\Code\Test Logs', FolderList(1).name));
str8 = strcat('Directory Orbt: ', fullfile(' C:\Users\jack.kolker\Desktop\Summer 2022\Code\Test Logs', FolderList(2).name));
disp(str4);
disp(str5);
disp(str6);
disp(str7);
disp(str8);
