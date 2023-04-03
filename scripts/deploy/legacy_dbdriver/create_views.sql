use jftf_cmdb;
create or replace view getLastMetadataId as
    select metadataID from TestCaseMetadata
    where metadataId = (select max(metadataId) from TestCaseMetadata);
grant select on jftf_cmdb.getLastMetadataId to 'jftf'@'localhost';

create or replace view getLastTestReportInformationId as
    select testReportInformationId from TestReportInformation
    where testReportInformationId = (select max(testReportInformationId) from TestReportInformation);
grant select on jftf_cmdb.getLastTestReportInformationId to 'jftf'@'localhost';

create or replace function p_mId() returns integer deterministic no sql return @mId;
create or replace view getTestCaseMetadata as
    select testName,featureGroup,testGroup,testPath,testVersion from TestCaseMetadata
    where metadataId = p_mId();
grant select on jftf_cmdb.getTestCaseMetadata to 'jftf'@'localhost';

create or replace function p_tId() returns integer deterministic no sql return @tId;
create or replace view getTestCase as
    select metaDataId,firstExecution,lastExecution,executed from TestCases
    where testId = p_tId();
grant select on jftf_cmdb.getTestCase to 'jftf'@'localhost';

create or replace function p_trId() returns integer deterministic no sql return @trId;
create or replace view getTestReportInformation as
    select testReportInformationId, testId, startupTimestamp, endTimestamp, testDuration, errorMessages, loggerOutput, executionResult from TestReportInformation
    where testReportInformationId = p_trId();
grant select on jftf_cmdb.getTestReportInformation to 'jftf'@'localhost';

create or replace function p_t1Id() returns integer deterministic no sql return @t1Id;
create or replace view getTestReportInformationForTestId as
    select testReportInformationId, testId, startupTimestamp, endTimestamp, testDuration, errorMessages, loggerOutput, executionResult from TestReportInformation
    where testId = p_t1Id();
grant select on jftf_cmdb.getTestReportInformationForTestId to 'jftf'@'localhost';

create or replace view getTestCaseIds as
    select unique testId from TestCases;
grant select on jftf_cmdb.getTestCaseIds to 'jftf'@'localhost';

create or replace view getTestReportInformationIds as
    select unique testReportInformationId from TestReportInformation;
grant select on jftf_cmdb.getTestReportInformationIds to 'jftf'@'localhost';