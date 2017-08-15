# st2_cmk - Check_MK Event Handler Integration for StackStorm
Integrates with [Check_MK](https://mathias-kettner.com/check_mk.html) monitoring framework.

## Configurations steps

### Install st2_cmk pack on StackStorm
Install st2_cmk pack
```
st2 pack install https://github.com/rodrigollima/st2_cmk.git
```

### Configure st2_cmk to send events to StackStorm
1. Enable st2_cmk chatops notification
      ```
      st2 rule enable st2_cmk.notify_chat
      st2ctl reload --register-rules
      ```
2. Copy st2_cmk event handler listener and config file to Check_MK host.
      ```
      cp /opt/stackstorm/packs/st2_cmk/conf/st2_cmk.yaml /etc/st2_cmk.yaml
      cp /opt/stackstorm/packs/st2_cmk/conf/st2_cmk.py /omd/sites/<master>/local/share/check_mk/notifications/st2_cmk.py
      chown +x /opt/stackstorm/packs/st2_cmk/conf/st2_cmk.py /omd/sites/<master>/local/share/check_mk/notifications/st2_cmk.py
      ```
3. Configure StackStorm settings on [`st2_cmk.yaml`](/conf/st2_cmk.yaml).

4. Install handler dependencies on Check_MK host.

      ``` pip install -r /opt/stackstorm/packs/st2_cmk/requirements.txt ```

5. Create nagios command.

      edit

      ``` vim /omd/sites/<master>/etc/nagios/conf.d/commands.cfg ```
      
      add 

      ``` 
      define command{
          command_name st2_event_handler
          command_line python /omd/sites/aws/local/share/check_mk/notifications/st2_cmk.py /etc/st2_cmk.yaml "$SERVICEEVENTID$" "$SERVICEDESC$" "$SERVICESTATE$" "$SERVICESTATEID$" "$SERVICESTATETYPE$" "$SERVICEATTEMPT$" "$HOSTNAME$" "$SERVICEOUTPUT$"
      }
      ```

6. Enable check_mk event handler 

      edit
      
      ``` vim /omd/sites/<master>/etc/check_mk/main.mk ```

      add

      ```
      extra_service_conf["event_handler_enabled"]=[("1", ALL_HOSTS, ALL_SERVICES)]
      extra_service_conf["event_handler"]=[("run_event_handler",ALL_HOSTS,ALL_SERVICES)]
      ```

      restart

      ``` cmk -O ```

      monitoring

      ``` tail -f  /omd/sites/<master>/var/log/nagios.log ```

      