"""
Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
"""
import six
from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch


class DependsOn(CloudFormationLintRule):
    """Check Base Resource Configuration"""
    id = 'E3005'
    shortdesc = 'Check DependsOn values for Resources'
    description = 'Check that the DependsOn values are valid'
    source_url = 'https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-dependson.html'
    tags = ['resources', 'dependson']

    def check_value(self, key, path, resources):
        """Check resource names for DependsOn"""
        matches = []

        if not isinstance(key, (six.text_type, six.string_types)):
            message = 'DependsOn values should be of string at {0}'
            matches.append(RuleMatch(path, message.format('/'.join(map(str, path)))))
            return matches
        if key not in resources:
            message = 'DependsOn should reference other resources at {0}'
            matches.append(RuleMatch(path, message.format('/'.join(map(str, path)))))

        return matches

    def match(self, cfn):
        """Check CloudFormation Resources"""

        matches = []

        resources = cfn.get_resources()

        for resource_name, resource_values in resources.items():
            depends_ons = resource_values.get('DependsOn')
            if depends_ons:
                path = ['Resources', resource_name, 'DependsOn']
                self.logger.debug('Validating DependsOn for %s base configuration', resource_name)
                if isinstance(depends_ons, list):
                    for index, depends_on in enumerate(depends_ons):
                        matches.extend(self.check_value(depends_on, path[:] + [index], resources))
                else:
                    matches.extend(self.check_value(depends_ons, path, resources))

        return matches
