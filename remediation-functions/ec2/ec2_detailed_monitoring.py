'''
Copyright (c) Cloudneeti. All rights reserved.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is  furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Enable detailed monitoring of ec2 instance
'''

from botocore.exceptions import ClientError

def run_remediation(ec2, Instance_name):
    print("Executing ec2 remediation")            

    detailed_monitoring = False
    try:
        response=ec2.describe_instances(InstanceIds=[Instance_name])['Reservations'][0]['Instances'][0]['Monitoring']  #review with lambda
        if response['State'] == 'enabled':
            detailed_monitoring = True
    except:
        detailed_monitoring=False

    if not detailed_monitoring:   
        try:
            result = ec2.monitor_instances(InstanceIds=[Instance_name])

            responseCode = result['ResponseMetadata']['HTTPStatusCode']
            if responseCode >= 400:
                output = "Unexpected error: %s \n" % str(result)
            else:
                output = "Detailed monitoring is enabled for ec2 instance : %s \n" % Instance_name
                    
        except ClientError as e:
            responseCode = 400
            output = "Unexpected error: " + str(e)
            print(output)
        except Exception as e:
            responseCode = 400
            output = "Unexpected error: " + str(e)
            print(output)
    else:
        responseCode=200
        output="Detailed monitoring is already enabled for ec2 instance  : %s \n" % Instance_name

    print(str(responseCode)+'-'+output)
    return responseCode,output