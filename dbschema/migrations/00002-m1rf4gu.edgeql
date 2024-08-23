CREATE MIGRATION m1rf4gu7li22oko5n4xxrem7atcewoor7q7kkcevyxeqok4iue4b6q
    ONTO m1g7jx5zmnbxvwyoaf6dggmlxkd7idj5imo3emuza75jcp2vr7jaoq
{
  ALTER TYPE default::counter {
      CREATE PROPERTY name: std::str;
      ALTER PROPERTY uuid {
          CREATE CONSTRAINT std::exclusive;
          SET REQUIRED USING (<std::uuid>{});
      };
  };
};
